# QA runner image. Built by deploy.sh from a staged context that holds only
# skills/qa/, knowledge-base/, CLAUDE.md, README.txt, FOLDER_INDEX.md and
# .claude/hooks — never outputs/, archive/ or any credentials.
FROM node:22-bookworm-slim

# Pin to a tested Claude Code release once the first run passes.
ARG CLAUDE_CODE_VERSION=latest

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv jq git ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g "@anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}"

COPY skills/qa/container/requirements.txt /tmp/requirements.txt
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt
ENV PATH="/opt/venv/bin:${PATH}"

# Claude Code refuses bypassPermissions as root.
RUN useradd --create-home --shell /bin/bash qa
WORKDIR /workspace
COPY --chown=qa:qa . /workspace

# The container's settings replace the Mac ones (auto-sync and ~/.claude hooks
# do not exist here). Skills are discovered through .claude/skills symlinks,
# the same layout README.txt describes for a fresh machine.
# Knowledge Base slices are generated from the Knowledge Base in this image, so
# they can never drift from it. The build fails if an exclusion no longer
# matches exactly one heading.
RUN python3 skills/qa/container/kb_slices.py

# The robustness tests (slices, narrowed reads, Certify summary, delivery gate,
# ledger, parity logic, Max's findings-never-block test) gate the image: a
# change that weakens any of them cannot be deployed.
RUN python3 skills/qa/container/tests/test_container.py

RUN cp skills/qa/container/settings.json .claude/settings.json \
 && mkdir -p .claude/skills outputs/qa \
 && for d in skills/qa/*/; do \
      n="$(basename "$d")"; \
      if [ -f "$d/SKILL.md" ]; then ln -sfn "../../skills/qa/$n" ".claude/skills/$n"; fi; \
    done \
 && chown -R qa:qa /workspace

USER qa
ENV QA_WORKSPACE=/workspace CLAUDE_PROJECT_DIR=/workspace ISOMETRIC_ENV=prod
ENTRYPOINT ["python3", "/workspace/skills/qa/container/entrypoint.py"]
