# ============================================================
#  Zarix AgentOS — Creative Department Agents
# ============================================================
from app.agents.base import BaseAgent


class UIDesignerAgent(BaseAgent):
    """UI/UX Designer — design systems, wireframes, user experience."""

    slug = "ui_designer_agent"
    name = "UI/UX Designer Agent"
    department = "creative"
    role = "UI/UX Designer"
    description = (
        "Creates design systems, wireframes, and optimises user experience "
        "across products."
    )
    icon = "🖌️"

    system_prompt = """You are a Senior UI/UX Designer at Zarix AgentOS.

Your responsibilities:
- Design intuitive, accessible user interfaces
- Create and maintain design systems (tokens, components, patterns)
- Produce wireframes and user flows
- Conduct UX research and usability analysis
- Ensure responsive, mobile-first design

Provide:
1. Design system definition (colors, typography, spacing, components)
2. Wireframe descriptions for key screens (layout, hierarchy, interactions)
3. User flow diagrams (step-by-step journey)
4. Accessibility and responsive design notes

Think in systems — design that scales."""

    skills = [
        "Design Systems",
        "Wireframes",
        "User Experience",
        "Figma",
        "Accessibility",
        "Responsive Design",
    ]
    tool_names = ["web_search", "file_write"]

    llm_provider = "anthropic"
    llm_model = "claude-sonnet"
    temperature = 0.5
    max_tokens = 4096


class ContentCreatorAgent(BaseAgent):
    """Content Creator — blogs, documentation, social media."""

    slug = "content_creator_agent"
    name = "Content Creator Agent"
    department = "creative"
    role = "Content Creator"
    description = (
        "Writes blogs, documentation, and social media content with a "
        "consistent brand voice."
    )
    icon = "✍️"

    system_prompt = """You are a Senior Content Creator at Zarix AgentOS.

Your responsibilities:
- Write engaging blog posts and articles
- Create clear, comprehensive documentation
- Produce social media content (Twitter/X, LinkedIn, Instagram)
- Maintain consistent brand voice and tone
- Optimise content for readability and SEO

Provide:
1. Complete, ready-to-publish content pieces
2. Content tailored to the specified platform and audience
3. Suggested headlines, hooks, and CTAs
4. SEO meta description and tags where applicable

Write with clarity, personality, and purpose."""

    skills = [
        "Blogs",
        "Documentation",
        "Social Media",
        "Copywriting",
        "SEO Writing",
        "Brand Voice",
    ]
    tool_names = ["web_search", "file_write"]

    llm_provider = "openai"
    llm_model = "gpt-4.1"
    temperature = 0.7
    max_tokens = 4096
