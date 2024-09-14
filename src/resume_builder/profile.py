from dataclasses import dataclass
from typing import List

@dataclass
class Experience:
    title: str
    company: str
    date_range: str
    description: List[str]

@dataclass
class Education:
    degree: str
    school: str
    graduation_year: str
    details: str

@dataclass
class Project:
    title: str
    description: str

@dataclass
class Organization:
    name: str
    role: str

@dataclass
class ProfileInfo:
    name: str
    title: str
    email: str
    phone: str
    linkedin: str
    github: str
    profile_summary: str
    experiences: List[Experience]
    education: List[Education]
    skills: List[str]
    certifications: List[str]
    projects: List[Project]
    languages: List[str]
    organizations: List[Organization]