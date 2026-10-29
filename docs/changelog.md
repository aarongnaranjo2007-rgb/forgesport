---
title: Changelog
---
# Changelog

Una entrada por commit, agrupadas por año.

{% for page in site.pages %}
{% if page.path contains 'changelog/' %}
- [{{ page.title }}]({{ page.url | relative_url }})
{% endif %}
{% endfor %}
