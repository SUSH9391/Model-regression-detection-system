import JobTile from './JobTile'

const EXPERIENCE = [
  {
    title: 'Backend Engineer Intern',
    company: 'Tech Corp Inc.',
    date: 'Jun – Aug 2024',
    shift: 'right',
    description:
      'Developed RESTful APIs in Node.js and Express, improving response time by 40%. Collaborated with the DevOps team to containerize services using Docker and deploy to AWS ECS.',
  },
  {
    title: 'Software Developer Co-op',
    company: 'Innovatech Solutions',
    date: 'Jan – Apr 2024',
    shift: 'left',
    description:
      'Built internal tooling dashboards with React and integrated them with a Python Flask backend. Automated CI/CD pipelines using GitHub Actions, reducing deployment time by 60%.',
  },
  {
    title: 'Research Assistant',
    company: 'University Lab — AI & Vision',
    date: 'Sep – Dec 2023',
    shift: 'right',
    description:
      'Assisted in developing a computer vision pipeline for real-time object detection using PyTorch and OpenCV. Published findings in a departmental proceedings paper.',
  },
]

const EDUCATION = [
  {
    title: 'B.Eng. Computer Engineering',
    company: 'University of Technology',
    date: '2021 – 2025',
    shift: 'left',
    description:
      'Major in Computer Engineering with a focus on Systems and Software. Relevant coursework: Algorithms, Operating Systems, Machine Learning, Distributed Systems.',
  },
]

export default function Resume() {
  return (
    <div className="resumePage">
      <div className="middleLine" aria-hidden="true" />

      <h1>RESUME</h1>

      {/* Experience */}
      <h2>Experience</h2>
      <div className="jobContainer">
        {EXPERIENCE.map((job) => (
          <JobTile key={job.title} {...job} />
        ))}
      </div>

      {/* Education */}
      <h2>Education</h2>
      <div className="jobContainer">
        {EDUCATION.map((edu) => (
          <JobTile key={edu.title} {...edu} />
        ))}
      </div>

      {/* Download CTA */}
      <a
        href="/resume.pdf"
        target="_blank"
        rel="noopener noreferrer"
        className="pillBtn"
        style={{ marginTop: '40px', padding: '12px 36px', fontSize: '1rem' }}
      >
        Download PDF ↗
      </a>
    </div>
  )
}
