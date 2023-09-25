# Corpus Creation Interface

This folder contains the web interface (in Portuguese) for the gathering of puns in the BRHuM corpus project.

## How to use

The interface is entirely implemented in pure HTML and JS. This means that it can be run by only opening `index.html` in a browser.

As the interface is simpler, it does not have any access to local or remote files, unless the user uploads it directly at the top of the page. The uploaded file should be in the JSON format specified in the [guidelines](../data/GUIDELINES.md).

Every single pun is registered to a JSON format string that can be downloaded or copied to the clipboard on the bottom part of the page.

IDs are automatically added based on the Source ID provided during the registration. IDs are in the format `sourceID.punID`.
