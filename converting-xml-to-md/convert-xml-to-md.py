import os
import json
import sys
from loguru import logger
import xml.etree.ElementTree as ET
import unicodedata
import string
from jinja2 import Template
import jinja2
import markdown

logger.add(
    sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>"
)


valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


def clean_filename(filename, whitelist=valid_filename_chars, replace=" "):
    # replace spaces
    for r in replace:
        filename = filename.replace(r, "_")

    # keep only valid ascii chars
    cleaned_filename = (
        unicodedata.normalize("NFKD", filename).encode("ASCII", "ignore").decode()
    )

    # keep only whitelisted chars
    cleaned_filename = "".join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename) > char_limit:
        print(
            "Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(
                char_limit
            )
        )
    return cleaned_filename[:char_limit]


path = "./docs/"


def make_markdown_from_xml():
    try:
        for filename in os.listdir(path):
            if filename.endswith(".xml"):

                dict = {}

                # Make an output filename to match the input
                filepath = os.path.join(path, filename)
                txt_file_path = filepath.replace(".xml", ".txt")
                markdown_filename = filepath.split("/")[2]
                markdown_filename = markdown_filename.split(".")[0]
                markdown_output_filepath = (
                    "./markdown_output/" + markdown_filename + ".md"
                )

                # load and parse the XML file for key and values
                xmlTree = ET.parse(filepath)

                for elem in xmlTree.iter():
                    if elem.text is not None:

                        key = elem.tag
                        value = elem.text.replace(
                            ":", " "
                        )  # removing colons from text areas since markdown
                        if ("pdf_file") in key:
                            value = clean_filename(value)

                        dict[key] = value

                        # json_string = json.dumps(kv)
                        #
                        # # removing JSON since needs to be plaintext
                        # def remove_json_chars(json_string):
                        #     no_json_string = json_string.replace("}", "").replace(
                        #         "{", ""
                        #     )
                        #     cleaned_string = no_json_string.replace('"', "")
                        #     return cleaned_string
                        #
                        # string = remove_json_chars(json_string)
                        #
                        # if ("pdf_file") in key:
                        #     r.rec("resources:")
                        #     value = remove_json_chars(value)
                        #     url_pair = "url: " + value
                        #     r.rec(url_pair)
                        #
                        # r.rec(string)

                # end of elemTree iteration

                # Populating variables for Jinja template to make precise Markdown
                PacELF_ID = dict.get("PacELF_ID", "N/A")
                title = dict.get("title", "N/A")
                type = dict.get("type", "N/A")
                authors = dict.get("authors", "N/A")
                description = dict.get("description", "N/A")
                category = dict.get("category", "N/A")
                pdf_file_name = dict.get("pdf_file_name", "N/A")
                access_rights = dict.get("access_rights", "N/A")
                hardcopy_location = dict.get("hardcopy_location", "N/A")
                pages = dict.get("pages", "N/A")
                work_location = dict.get("work_location", "N/A")
                language = dict.get("language", "N/A")
                year = dict.get("year", "N/A")
                decade = dict.get("decade", "N/A")
                journal = dict.get("journal", "N/A")
                publisher = dict.get("publisher", "N/A")

                # Experimenting with markdown generation

                template = Template(
                    "---\n"
                    "schema: pacelf\n"
                    "title: {{ title }}\n"
                    "organization: {{ authors }}\n"
                    "notes: {{ description }}\n"
                    "url: '{{ pdf_file_name }}'\n"
                    "\n"
                    "resources:\n"
                    "- name: {{ title }}\n"
                    "url: '{{ pdf_file_name }}'\n"
                    "format: {{ type }}\n"
                    "access: {{ access_rights }}\n"
                    "pages: {{ pages }}\n"
                    " \n"
                    "category: {{ category }}\n"
                    "journal: {{ journal }}\n"
                    "publisher: {{ publisher }}\n"
                    "language: {{ language }} \n"
                    "hardcopy_location: {{ hardcopy_location }}\n"
                    "work_location: {{ work_location }}\n"
                    "year: {{ year }}\n"
                    "decade: {{ decade }}\n"
                    "PacELF_ID: {{ PacELF_ID }}\n"
                    "---"
                )
                rendered_template = template.render(
                    title=title,
                    PacELF_ID=PacELF_ID,
                    type=type,
                    authors=authors,
                    description=description,
                    category=category,
                    pdf_file_name=pdf_file_name,
                    access_rights=access_rights,
                    hardcopy_location=hardcopy_location,
                    pages=pages,
                    work_location=work_location,
                    language=language,
                    year=year,
                    decade=decade,
                    journal=journal,
                    publisher=publisher,
                )

                # print(rendered_template)
                # logger.info(rendered_template)

                # attempts to clean up markdown in a code block
                # def markup(text, *args, **kwargs):
                #     return markdown(text, *args, **kwargs)
                #
                # marked_template = markup(rendered_template)
                # marked_template = marked_template.replace("<pre><code>", "")
                # marked_template = marked_template.replace("<pre><code>", "").replace(
                #     "</code></pre>", ""
                # )

                with open(markdown_output_filepath, "w") as text_file:
                    print(rendered_template, file=text_file)

        # can remove duplicates - convert to set and back to list
        # elemList = list(set(elemList))

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    make_markdown_from_xml()
