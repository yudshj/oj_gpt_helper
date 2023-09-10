# MyType struct
from dataclasses import dataclass, field

@dataclass
class ProblemInfo:
    problem_description: str = ""
    input_description: str = ""
    output_description: str = ""
    sample_input_description: str = ""
    sample_output_description: str = ""

@dataclass
class SubmissionInfo:
    source_code: str = ""
    problem_info: ProblemInfo = field(default_factory=ProblemInfo)
    status: str = ""
    username: str = ""
    language: str = ""
