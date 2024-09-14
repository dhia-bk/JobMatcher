from profile import ProfileInfo

class ResumeBuilder:
    def __init__(self, profile_info: ProfileInfo):
        self.profile_info = profile_info

    def generate_html(self):
        css = """ * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #000; /* Changed to black */
            background-color: #fff;
            padding: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 36px;
            margin-bottom: 5px;
            display: inline-block;
        }

        .header .title {
            font-size: 24px; /* Slightly smaller font for title */
            color: #000;
            display: inline-block;
            margin-left: 10px;
        }

        .header p {
            font-size: 18px;
            color: #000;
        }

        .section {
            margin-bottom: 25px;
        }

        .section-title {
            color: #000;
            font-size: 22px;
            margin-bottom: 15px;
            border-bottom: 2px solid #000; /* Changed to black */
            padding-bottom: 5px;
        }

        ul {
            list-style-type: disc; /* Changed to bullet points */
            padding-left: 20px;
        }

        li {
            margin-bottom: 15px;
        }

        .experience, .education {
            padding-left: 10px;
        }

        .job-title {
            font-weight: bold;
            color: #000; /* Changed to black */
        }

        .company {
            color: #000; /* Changed to black */
        }

        .date {
            float: right;
            color: #000; /* Changed to black */
        }

        .skills-list {
            display: inline;
        }

        .skills-list span {
            margin-right: 15px;
            font-weight: bold;
            color: #000; /* Changed to black */
        }

        a {
            color: #000; /* Changed to black */
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            font-size: 14px;
            color: #000; /* Changed to black */
        }
        """
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resume - {self.profile_info.name}</title>
            <style>{css}</style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{self.profile_info.name}</h1>
                    <p class="title">{self.profile_info.title}</p>
                    <p>Email: {self.profile_info.email} | Phone: {self.profile_info.phone} | 
                    <a href='{self.profile_info.linkedin}' target='_blank'>LinkedIn</a> | 
                    <a href='{self.profile_info.github}' target='_blank'>GitHub</a></p>
                </div>

                <div class="section">
                    <h2 class="section-title">Profile</h2>
                    <p>{self.profile_info.profile_summary}</p>
                </div>

                <div class="section">
                    <h2 class="section-title">Experience</h2>
                    <ul>
        """
        for exp in self.profile_info.experiences:
            html += f"""
                <li>
                    <span class='job-title'>{exp.title}</span> at 
                    <span class='company'>{exp.company}</span>
                    <span class='date'>{exp.date_range}</span>
                    <ul>
                        <li>{exp.description}</li>
                    </ul>
                </li>
            """

        html += """
                    </ul>
                </div>

                <div class="section">
                    <h2 class="section-title">Education</h2>
                    <ul>
        """
        for edu in self.profile_info.education:
            html += f"""
                <li>
                    <span class='job-title'>{edu.degree}</span> - 
                    <span class='company'>{edu.school}</span>
                    <span class='date'>{edu.graduation_year}</span>
                    <p>{edu.details}</p>
                </li>
            """

        html += """
                    </ul>
                </div>

                <div class="section">
                    <h2 class="section-title">Skills</h2>
                    <div class="skills">
        """
        for skill in self.profile_info.skills:
            html += f"<span class='skill'>{skill}</span> "

        html += """
                    </div>
                </div>

                <div class="section">
                    <h2 class="section-title">Certifications</h2>
                    <ul>
        """
        for cert in self.profile_info.certifications:
            html += f"<li>{cert}</li>"

        html += """
                    </ul>
                </div>

                <div class="section">
                    <h2 class="section-title">Projects</h2>
                    <ul>
        """
        for project in self.profile_info.projects:
            html += f"<li><span class='job-title'>{project.title}</span> - {project.description}</li>"

        html += """
                    </ul>
                </div>

                <div class="section">
                    <h2 class="section-title">Languages</h2>
                    <div>
        """
        for language in self.profile_info.languages:
            html += f"<a>{language} </a>"

        html += """
                    </div>
                </div>

                <div class="section">
                    <h2 class="section-title">Organizations</h2>
                    <ul>
        """
        for org in self.profile_info.organizations:
            html += f"<li><span class='job-title'>{org.role}</span> at {org.name}</li>"

        html += """
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
        return html
