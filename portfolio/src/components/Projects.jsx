import ProjectTile from './ProjectTile'

const PROJECTS = [
  {
    name: 'Regression\nDetector',
    subtitle: 'Model Regression Detection System',
    tech: ['Python', 'DeepEval', 'FastAPI', 'Docker', 'GitHub Actions'],
    description:
      'An automated pipeline that evaluates LLM output quality across releases, flags regressions using statistical thresholds, and posts CI reports to GitHub.',
    image: 'https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=800&q=80',
    githubUrl: 'https://github.com/shadmansohel',
    liveUrl: null,
  },
  {
    name: 'Cloud\nGateway',
    subtitle: 'Microservices API Gateway',
    tech: ['Go', 'gRPC', 'Docker', 'Kubernetes', 'Prometheus'],
    description:
      'A high-throughput API gateway in Go that routes traffic across microservices, enforces rate limits, and exposes Prometheus metrics for observability.',
    image: 'https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&q=80',
    githubUrl: 'https://github.com/shadmansohel',
    liveUrl: 'https://example.com',
  },
  {
    name: 'Real-Time\nDashboard',
    subtitle: 'Live Analytics Dashboard',
    tech: ['React', 'Node.js', 'WebSockets', 'MongoDB', 'Chart.js'],
    description:
      'A real-time analytics dashboard that streams event data via WebSockets and renders interactive charts with sub-100ms latency.',
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80',
    githubUrl: 'https://github.com/shadmansohel',
    liveUrl: 'https://example.com',
  },
  {
    name: 'Vision\nPipeline',
    subtitle: 'Real-Time Object Detection',
    tech: ['Python', 'PyTorch', 'OpenCV', 'ONNX', 'FastAPI'],
    description:
      'A computer-vision pipeline that runs YOLOv8 inference on video streams, optimised for edge deployment with ONNX runtime quantisation.',
    image: 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800&q=80',
    githubUrl: 'https://github.com/shadmansohel',
    liveUrl: null,
  },
]

export default function Projects() {
  return (
    <div className="projectsPage">
      <h1>PROJECTS</h1>
      <div className="projectsContainerPage">
        {PROJECTS.map((p) => (
          <ProjectTile key={p.name} {...p} />
        ))}
      </div>
    </div>
  )
}
