import { Link } from 'react-router-dom'
import FeaturedProjectCard from './FeaturedProjectCard'

// Stagger delay per letter
function AnimatedTitle({ text }) {
  return (
    <h1 className="bigTitle">
      {text.split('').map((char, i) => (
        <span
          key={i}
          className="letterAnimation"
          style={{ animationDelay: `${i * 0.1}s` }}
        >
          {char}
        </span>
      ))}
    </h1>
  )
}

const FEATURED = [
  {
    title: 'Model Regression Detection',
    subtitle: 'AI / ML · Python',
    image: 'https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=600&q=80',
  },
  {
    title: 'Real-Time Dashboard',
    subtitle: 'React · Node.js · WebSockets',
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=80',
  },
  {
    title: 'Cloud API Gateway',
    subtitle: 'Go · Docker · Kubernetes',
    image: 'https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=600&q=80',
  },
]

export default function Home() {
  return (
    <>
      {/* ── Landing Face ───────────────────────────────── */}
      <section className="landingPageFace" aria-label="Landing">
        <div className="leftOfFace">
          <AnimatedTitle text="SHADMAN" />
          <AnimatedTitle text="SOHEL" />
        </div>

        <div className="profileContainer">
          <img
            className="profileImg"
            src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&q=80"
            alt="Profile photo"
          />
          <Link to="/resume">
            <button className="pillBtn">Resume</button>
          </Link>
        </div>
      </section>

      {/* ── About Me ───────────────────────────────────── */}
      <section className="landingPageContainer" aria-label="About Me">
        <h1>ABOUT ME</h1>
        <p>
          Computer Engineering student passionate about backend development,
          machine learning, and building products that scale. Currently seeking
          internship opportunities to bring ideas from prototype to production.
        </p>
      </section>

      {/* ── Featured Projects ───────────────────────────── */}
      <section className="featuredProjects" aria-label="Featured Projects">
        <h1>FEATURED PROJECTS</h1>
        <div className="projectsContainer">
          {FEATURED.map((p) => (
            <FeaturedProjectCard key={p.title} {...p} />
          ))}
        </div>
      </section>
    </>
  )
}
