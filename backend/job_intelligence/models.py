from django.conf import settings
from django.db import models



class Company(models.Model):
    """Represent a company connected to job postings."""

    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(max_length=1000, blank=True)
    summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name



class SkillManager(models.Manager):
    """Manage Skill creation from raw skill names."""

    def get_or_create_from_name(self, name: str):
        """Return an existing skill or create one from a raw skill name."""
        from job_intelligence.services.skills import (
            guess_skill_category,
            normalize_skill_name,
            prettify_skill_name,
        )

        normalized_name = normalize_skill_name(name)
        display_name = prettify_skill_name(normalized_name)
        category = guess_skill_category(normalized_name)

        # use the get_or_create provided by models.manager with the custom categorization names
        return self.get_or_create(
            normalized_name=normalized_name,
            defaults={
                "name": display_name,
                "category": category,
            },
        )



class Skill(models.Model):
    """Represent a skill found in job postings."""

    class SkillCategory(models.TextChoices):
        PROGRAMMING_LANGUAGE = "programming_language", "Programming language"
        FRAMEWORK = "framework", "Framework"
        DATABASE = "database", "Database"
        CLOUD = "cloud", "Cloud"
        DEVOPS = "devops", "DevOps"
        FRONTEND = "frontend", "Frontend"
        BACKEND = "backend", "Backend"
        DATA = "data", "Data"
        MACHINE_LEARNING = "machine_learning", "Machine learning"
        SOFT_SKILL = "soft_skill", "Soft skill"
        TOOL = "tool", "Tool"
        OTHER = "other", "Other"

    name = models.CharField(max_length=100, unique=True)
    normalized_name = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
    )
    category = models.CharField(
        max_length=50,
        choices=SkillCategory.choices,
        default=SkillCategory.OTHER,
    )

    # overwritting the default manager ('objects') django models.Model provides
    objects = SkillManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["normalized_name"]

    # Skill.objects.create(name="c++") passes trhough this code at the end
    def save(self, *args, **kwargs):
        """Normalize skill fields before saving."""
        from job_intelligence.services.skills import (
            guess_skill_category,
            normalize_skill_name,
            prettify_skill_name,
        )

        self.normalized_name = normalize_skill_name(self.name)
        self.name = prettify_skill_name(self.normalized_name)

        if self.category == self.SkillCategory.OTHER:
            self.category = guess_skill_category(self.normalized_name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class JobPosting(models.Model):
    """Represent one saved job posting from a job board or company site."""

    class WorkMode(models.TextChoices):
        ONSITE = "onsite", "On-site"
        REMOTE = "remote", "Remote"
        HYBRID = "hybrid", "Hybrid"
        UNKNOWN = "unknown", "Unknown"

    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full-time"
        PART_TIME = "part_time", "Part-time"
        CONTRACT = "contract", "Contract"
        INTERNSHIP = "internship", "Internship"
        UNKNOWN = "unknown", "Unknown"

    class ExperienceLevel(models.TextChoices):
        INTERN = "intern", "Intern"
        ENTRY_LEVEL = "entry_level", "Entry level"
        JUNIOR = "junior", "Junior"
        MID_LEVEL = "mid_level", "Mid-level"
        SENIOR = "senior", "Senior"
        UNKNOWN = "unknown", "Unknown"

    class JobFunction(models.TextChoices):
        BACKEND = "backend", "Backend"
        FRONTEND = "frontend", "Frontend"
        FULL_STACK = "full_stack", "Full stack"
        DATA_ANALYTICS = "data_analytics", "Data analytics"
        DATA_ENGINEERING = "data_engineering", "Data engineering"
        MACHINE_LEARNING = "machine_learning", "Machine learning"
        DEVOPS = "devops", "DevOps"
        QA = "qa", "QA"
        CYBERSECURITY = "cybersecurity", "Cybersecurity"
        UNKNOWN = "unknown", "Unknown"

    class SalaryPeriod(models.TextChoices):
        HOUR = "hour", "Hour"
        YEAR = "year", "Year"
        UNKNOWN = "unknown", "Unknown"

    # Basic
    title = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="job_postings", # company.job_posting acessible now too
    )
    source_url = models.URLField(max_length=1000, blank=True)
    source_site = models.CharField(max_length=100, blank=True)

    # Location
    location_text = models.CharField(max_length=255, blank=True)
    work_mode = models.CharField(
        max_length=20,
        choices=WorkMode.choices,
        default=WorkMode.UNKNOWN,
    )

    # Classification
    employment_type = models.CharField(
        max_length=30,
        choices=EmploymentType.choices,
        default=EmploymentType.UNKNOWN,
    )
    experience_level = models.CharField(
        max_length=30,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.UNKNOWN,
    )
    job_function = models.CharField(
        max_length=50,
        choices=JobFunction.choices,
        default=JobFunction.UNKNOWN,
    )

    # Compensation
    salary_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    salary_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    salary_currency = models.CharField(max_length=10, default="USD")
    salary_period = models.CharField(
        max_length=20,
        choices=SalaryPeriod.choices,
        default=SalaryPeriod.UNKNOWN,
    )

    # Content
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    raw_text = models.TextField(blank=True)

    # Dates
    date_posted = models.DateField(null=True, blank=True)
    date_found = models.DateField(auto_now_add=True)

    # Relationships
    skills = models.ManyToManyField(
        Skill,
        # using JobPostingSkillRequirement as the join table between skill and jobposting
        through="JobPostingSkillRequirement",
        related_name="job_postings",
        blank=True,
    )

    # System
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_postings",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} at {self.company.name}"



class JobPostingSkillRequirement(models.Model):
    """Represent how a skill appears in a job posting."""

    class RequirementLevel(models.TextChoices):
        REQUIRED = "required", "Required"
        PREFERRED = "preferred", "Preferred"
        MENTIONED = "mentioned", "Mentioned"
        UNKNOWN = "unknown", "Unknown"

    job_posting = models.ForeignKey( # many to one
        JobPosting,
        on_delete=models.CASCADE,
        related_name="skill_requirements",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="job_posting_requirements",
    )
    requirement_level = models.CharField(
        max_length=20,
        choices=RequirementLevel.choices,
        default=RequirementLevel.UNKNOWN,
    )
    source_text = models.CharField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["requirement_level", "skill__normalized_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["job_posting", "skill"],
                name="unique_skill_requirement_per_job_posting",
            )
        ]

    def __str__(self):
        return (
            f"{self.skill.name} "
            f"({self.get_requirement_level_display()}) "
            f"for {self.job_posting}"
        )



class Application(models.Model):
    """Represent a user's application to a saved job posting."""

    class Status(models.TextChoices):
        SAVED = "saved", "Saved"
        APPLIED = "applied", "Applied"
        RECRUITER_SCREEN = "recruiter_screen", "Recruiter screen"
        INTERVIEW = "interview", "Interview"
        TECHNICAL_INTERVIEW = "technical_interview", "Technical interview"
        FINAL_INTERVIEW = "final_interview", "Final interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"
        GHOSTED = "ghosted", "Ghosted"
        ARCHIVED = "archived", "Archived"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    job_posting = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.SAVED,
    )
    date_applied = models.DateField(null=True, blank=True)
    last_contact_date = models.DateField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)

    match_score = models.PositiveSmallIntegerField(null=True, blank=True)
    interest_level = models.PositiveSmallIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                # The user field and job_posting field together must be unique.
                fields=["user", "job_posting"],
                name="unique_application_per_user_job_posting", # db constrain name.
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.job_posting}"