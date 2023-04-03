import json
from typing import List
# Each annotated entity contains:
#   EntityType: the annotated entity
#   EntityValue: the annotated report substring
#   begin/end: defines the bounderies of entity value within the text.
class Entity():
    def __init__(self, entity_type: str, value: str, begin: int):
        self.type = entity_type
        self.value = value
        self.begin = begin

    def as_json(self):
        return json.dumps(
            {
             'Entity': self.type,
             'Value': self.value,
             'begin': self.begin
            },
            indent=2, ensure_ascii=False
        )
    def as_dict(self):
        return {
            'Entity': self.type,
            'Value': self.value,
            'begin': self.begin,
        }

class InvalidReportError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

# Process the annotated entities that are in brackets format,
# transforming the report back into their original version and
# removing the annotated metadata into json key:value pairs.
# input_json: list with all annotated reports.
class EntityProcessor():
    def __init__(self, data):
        self._input = data

    def _run_entity_extraction_unit_tests(self):
        string_example = "[Entity](this is the entity value)"
        (result_string, result_entities) = self._extract_entities_from_report(string_example)
        # print(result_entities[0].as_json())
        assert result_entities[0].type == "Entity"
        assert result_entities[0].value == "this is the entity value"
        assert result_entities[0].begin == 0

        string_example = "[Entity](this is the [Entity2](another entity) value with another entity inside)"
                        #"this is the another entity value with another entity inside"
        (result_string, result_entities) = self._extract_entities_from_report(string_example)
        assert len(result_entities) == 2
        assert result_entities[1].type == "Entity"
        assert result_entities[1].value == "this is the another entity value with another entity inside"
        assert result_entities[1].begin == 0

        assert result_entities[0].type == "Entity2"
        assert result_entities[0].value == "another entity"
        assert result_entities[0].begin == 12
        # print(result_entities[0].as_json())

        string_example = "[Entity](this is the entity1 with [Entity2](entity2) and [Entity3](entity3) inside)"
                        #"this is the entity1 with entity2 and entity3 inside"
        (result_string, result_entities) = self._extract_entities_from_report(string_example)
        assert len(result_entities) == 3
        # print(result_entities[0].as_json())
        assert len(result_entities) == 3
        assert result_entities[0].type == "Entity2"
        assert result_entities[0].value == "entity2"
        assert result_entities[0].begin == 25
        
        assert result_entities[1].type == "Entity3"
        assert result_entities[1].value == "entity3"
        assert result_entities[1].begin == 37        

        assert result_entities[2].type == "Entity"
        assert result_entities[2].value == "this is the entity1 with entity2 and entity3 inside"
        assert result_entities[2].begin == 0

        string_example = "regular text [Ent1](this [Enty22](entity2 [Entity333](entity3) inside) also() [Entity4](entity4))"
                        #  "regular text this entity2 entity3 inside also entity4"
        (result_string, result_entities) = self._extract_entities_from_report(string_example)
        # print(result_entities[0].as_json())
        assert len(result_entities) == 4
        assert result_entities[0].type == "Entity333"
        assert result_entities[0].value == "entity3"
        assert result_entities[0].begin == 26
        
        assert result_entities[1].type == "Enty22"
        assert result_entities[1].value == "entity2 entity3 inside"
        assert result_entities[1].begin == 18           

        assert result_entities[2].type == "Entity4"
        assert result_entities[2].value == "entity4"
        assert result_entities[2].begin == 48 

        assert result_entities[3].type == "Ent1"
        assert result_entities[3].value == "this entity2 entity3 inside also() entity4"
        assert result_entities[3].begin == 13
        assert result_string == "regular text this entity2 entity3 inside also() entity4"

        string_example = "this is a text without entity."
        (result_string, result_entities) = self._extract_entities_from_report(string_example)
        assert len(result_entities) == 0
        assert result_string == "this is a text without entity."

        string_example = ""
        (result_string, result_entities) = self._extract_entities_from_report(string_example)
        assert len(result_entities) == 0
        assert result_string == ""

    # Returns the modified report and a list of entities.
    @staticmethod
    def _extract_entities_from_report(string: str) -> (str, List[Entity]):
        entities = []
        start_indexes = []
        stack = []
        start_type = -1
        entity_type = ''
        i = 0
        while(i < len(string)):
            if string[i] == "[":
                start_indexes.append(i)
                start_type = i+1
            elif string[i] == "]":
                entity_type = string[start_type:i]
            elif string[i] == "(":
                if i > 0 and string[i-1] == "]":
                    stack.append("["+entity_type+"](")
                else:
                    stack.append('(')
            elif string[i] == ")":
                removed = stack.pop()
                if removed != "(":
                    # The Entity string that's being closed. eg: [NoduleInfo](
                    entity_type = removed[1:][:-2]
                    start = start_indexes.pop()
                    prefix = string[:start]
                    suffix = string[i+1:]
                    value = string[start+len(removed):i]
                    # Logically pre-compute the amount of characters that will be removed later
                    # on the prefix of this entity to get the real start index.
                    deep_level = len(list(filter(lambda x: len(x)>1, stack)))
                    adjustment = sum([len(to_remove)+1 for to_remove in stack if len(to_remove)>1]) - deep_level
                    # Create Entity.
                    entities.append(Entity(entity_type, value, start - adjustment))
                    # Update string after removal from deep to shallow.
                    string = prefix + value + suffix
                    # Logically retract pointer to the same position after 
                    # updating string.
                    i = (start + len(value) - 1)
            i += 1 
        return string, entities

    # Make sure all reports are valid to be proccesed.
    def _validate_reports(self):
        for medicalReport in self._input:
            report = medicalReport["report"]
            par_stack = []
            bracket_stack = []
            for i, char in enumerate(report):
                if char == "(":
                    par_stack.append("(")
                if char == ")":
                    try:
                        par_stack.pop()
                    except IndexError:
                        raise InvalidReportError(f"Unbalanced parenthesys at report: {medicalReport['id']}")
                if char == "[":
                    bracket_stack.append("[")
                if char == "]":
                    try:
                        bracket_stack.pop()
                        if report[i+1] != "(":
                            raise InvalidReportError(f"Use of brackets outside entity annotation at report: {medicalReport['id']}")
                    except IndexError:
                        raise InvalidReportError(f"Unbalanced brackets at report: {medicalReport['id']}")
            if len(par_stack) != 0:
                raise InvalidReportError(f"Unbalanced parenthesys at report: {medicalReport['id']}")
            if len(bracket_stack) != 0:
                raise InvalidReportError(f"Unbalanced brackets at report: {medicalReport['id']}")

    def process(self):
        self._run_entity_extraction_unit_tests()
        self._validate_reports()
        for medicalReport in self._input:
            if medicalReport['isDone'] == True:
                extracted_report, entities = self._extract_entities_from_report(medicalReport['report'])
                medicalReport['report'] = extracted_report
                medicalReport['entities'] = [entity.as_dict() for entity in entities]
                print("Proccessed report: ", medicalReport['id'])

if __name__ == '__main__':
    # Writes the JSON file
    with open('documents.json', 'r', encoding='utf8') as f:
        data = json.load(f)
    processor = EntityProcessor(data)
    processor.process()
    with open('proccesed_documents.json', 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    