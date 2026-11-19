# Jie Hu — Academic Website

Source code for [Jie Hu's academic website](https://hujie007.github.io/). The site uses a sidebar profile and a main content column, with a home-page news feed and three research areas, each with its own publication list. It includes responsive layouts, readable typography, publication search, BibTeX downloads, and links to the CV and profile photo.

Content is maintained in Markdown and YAML. Routine updates do not require editing HTML or installing Ruby. Changes committed to `main` are built and published automatically through GitHub Actions.

## Website and Repository

- **Live website:** [hujie007.github.io](https://hujie007.github.io/)
- **Repository:** [hujie007/hujie007.github.io](https://github.com/hujie007/hujie007.github.io)
- **Routine updates:** Open the relevant source file, click the pencil icon to edit it, and select **Commit changes**. GitHub Actions will update the website.

## Key Files

| Content to update | File |
| --- | --- |
| Name, position, email, affiliation, Scholar link, and job market notice | `site.yml` |
| Website URL, search title, and Google Search Console verification | `site.yml` |
| Home-page biography | `content/about.md` |
| Research overview | `content/research.md` |
| Titles, summaries, and keywords for the three research areas | `data/research.yml` |
| Adaptive Transfer Learning introduction | `content/research-transfer.md` |
| Federated & Distributed Learning introduction | `content/research-federated.md` |
| Efficient & Reliable Statistical Learning introduction | `content/research-inference.md` |
| Journal reviewing and professional service | `content/service.md` |
| Publications, authors, venues, statuses, and paper links | `data/publications.yml` |
| Home-page news | `data/news.yml` |
| Teaching and education | `content/teaching.md` |
| Talks and conferences | `content/talks.md` |
| Software and code links | `data/software.yml` |
| CV | Replace `assets/pdf/Jie_Hu_CV.pdf`, keeping the same filename |
| Profile photo | Replace `assets/img/jie-hu.jpg`, keeping the same filename |
| Accent color | `accent_color` in `site.yml` |
| Fonts, spacing, and layout | `assets/css/jie-hu.css` |

The `dist/` directory is generated automatically. Edit the source files listed above; the next build will regenerate the website.

## Editing Text

For example, to update the biography:

1. Open `content/about.md` in the repository.
2. Click the pencil icon (**Edit file**).
3. Edit the text. Use **Preview** to check the Markdown formatting.
4. Select **Commit changes** to save. Commit to `main`, or merge your changes into `main` if you use a separate branch.
5. Wait for the Actions workflow to finish, then refresh the website.

Publishing is handled by the workflow. GitHub's Markdown preview shows text formatting; check the published page for the complete website layout.

## Adding a Publication

Add a complete entry to `data/publications.yml`. Each paper must have a unique integer `id`; the example below uses `29`.

```yaml
- id: 29
  title: 'Your new paper title'
  authors: 'Jie Hu, Coauthor Name, Yong Chen*'
  year: 2027
  venue: ''
  status: 'Working papers'
  topic: 'Transfer learning'
  areas: ['transfer']
  selected: false
  url: ''
  code: ''
  pdf: ''
  detail: 'Submitted'
```

- `status` must be one of `Published & accepted`, `Under revision`, or `Working papers`.
- For papers with `status: Published & accepted`, set `selected: true` to list them under **Selected Publications**, or `selected: false` to list them under **Other Publications**. Papers with the other statuses appear in **Under Revision** or **Working Papers**. The four sections and their counts update automatically.
- Use the filter buttons to show **All**, **Selected Publications**, **Under Revision**, **Working Papers**, or **Other Publications**. Other Publications appears last in both the buttons and the full list.
- `areas` determines which research pages include the paper. Use `transfer`, `federated`, or `inference`. For example, `areas: [transfer, federated]` includes it in both areas.
- All three research publication lists are generated from the same data. Enter each paper once; paper counts update automatically.
- `venue` is the journal or publication venue. Leave it empty when appropriate.
- `url` is the full `https://...` link to the article, DOI, or arXiv page.
- `code` is the full URL of the code repository. Leave it empty if no code is available.
- `pdf` can be a full PDF URL or a local path such as `assets/pdf/YourPaper.pdf`. Upload local PDFs to `assets/pdf/` first.
- `detail` can contain information such as `In press`, `Minor revision`, or volume and page numbers.
- `topic` can use an existing topic or a new one. Its label is included in publication searches.
- List authors in their usual name order, separated by commas. Use `†` for equal first authorship and `*` for corresponding authorship. Jie Hu's name is bolded automatically.

Use spaces for YAML indentation, not tabs. Put titles containing colons or other special characters in quotes. If a string contains a single quote, use double quotes around the full string.

## Updating News

Add new entries at the top of `data/news.yml`. Include `category`, `title`, `text`, and `url`; set `url` to `''` if no link is needed. The `text` field supports Markdown, including bold text, italics, and links.

```yaml
- date: 'Jan. 2027'
  category: 'Accepted'
  title: 'Paper title accepted by Journal Name'
  text: 'A brief description of the work.'
  url: 'publications/#paper-29'
```

## Updating the CV, Photo, and Profile Settings

- **CV:** Replace `assets/pdf/Jie_Hu_CV.pdf` with the new PDF, keeping the same path and filename.
- **Photo:** Replace `assets/img/jie-hu.jpg` with a new JPG. To use a PNG instead, also update the `portrait` path in `site.yml`.
- **Job market notice:** Set `job_market: false` in `site.yml` to hide the notice.
- **Accent color:** Change `accent_color` to a six-digit hex color such as `'#416b91'`. Keep the quotes and `#`.
- **Last updated date:** Edit `updated` in `site.yml`, for example, `'January 2027'`.
- **GitHub profile:** Edit or clear the `github` value in `site.yml`. It currently points to `https://github.com/hujie007`.
- **Search settings:** `site_url` is the public website address, `home_title` is the home-page search title, and `description` is the search description. Each build generates `sitemap.xml`, `robots.txt`, and canonical page URLs.
- **Google Search Console:** Add `https://hujie007.github.io/` as a URL-prefix property and choose HTML tag verification. Copy only the tag's `content` value into `google_site_verification` in `site.yml`. After deployment, complete verification in Search Console, submit `https://hujie007.github.io/sitemap.xml`, and request indexing of the homepage.
