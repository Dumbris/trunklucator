#!/bin/sh

## Docs here https://github.com/asciidoctor/docker-asciidoctor

docker run --rm -v $(pwd):/documents/ asciidoctor/docker-asciidoctor asciidoctor-pdf -D dist/pdf -a imagesdir=dist/pdf/assets/images -r asciidoctor-diagram *.adoc
docker run --rm -v $(pwd):/documents/ asciidoctor/docker-asciidoctor asciidoctor  -D dist/html -a imagesdir=dist/html/assets/images -r asciidoctor-diagram *.adoc
