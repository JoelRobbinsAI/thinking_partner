import os
import re
from datetime import datetime
from typing import Dict, List, Optional

class CanonicalMemory:
    """Manages persistent canonical memory across domains."""
    
    def __init__(self, base_path: str = "backend/workspaces/cognitive/canonical"):
        self.base_path = base_path
        self.domains = {
            "user": "user.md",
            "projects": "projects.md",
            "self": "self.md",
            "open_knowledge": "open_knowledge.md"
        }
        
    def read_domain(self, domain: str) -> str:
        """Read the current content of a canonical domain."""
        file_path = os.path.join(self.base_path, self.domains[domain])
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        return ""
    
    def write_domain(self, domain: str, content: str):
        """Write updated content to a canonical domain."""
        file_path = os.path.join(self.base_path, self.domains[domain])
        with open(file_path, 'w') as f:
            f.write(content)
    
    def get_domain_sections(self, domain: str) -> Dict[str, str]:
        """Parse a canonical domain file into sections."""
        content = self.read_domain(domain)
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            # Skip empty lines at start
            if not line.strip() and not current_section:
                continue
                
            if line.startswith('## '):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                # Start new section
                current_section = line[3:].strip()
                current_content = []
            elif line.startswith('# '):
                # Skip main title
                continue
            elif line.startswith('---'):
                # Skip metadata separator
                continue
            elif line.startswith('*Last updated'):
                # Skip metadata
                continue
            elif current_section:
                current_content.append(line)
                
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
            
        return sections
    
    def update_domain_section(self, domain: str, section: str, content: str):
        """Update a specific section of a canonical domain."""
        # Get existing sections
        sections = self.get_domain_sections(domain)
        
        # Update or add the section
        sections[section] = content
        
        # Rebuild the file with clean structure
        header = f"# {domain.title()} Memory\n\n"
        updated_content = header
        
        for section_name, section_content in sections.items():
            if section_content and section_content != "[To be populated]":
                updated_content += f"## {section_name}\n{section_content}\n\n"
            else:
                updated_content += f"## {section_name}\n[To be populated]\n\n"
        
        # Add single metadata line at the end
        updated_content += f"---\n*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        
        self.write_domain(domain, updated_content)
    
    def get_all_domains(self) -> Dict[str, str]:
        """Read all canonical domains."""
        return {domain: self.read_domain(domain) for domain in self.domains.keys()}