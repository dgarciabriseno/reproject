FROM condaforge/miniforge3:latest
ENV API_BASE="https://api.helioviewer.org"
COPY app /app
RUN conda env create -f /app/environment.yml
RUN adduser user
USER user
ENTRYPOINT ["/opt/conda/envs/reproject/bin/python"]
CMD ["/app/reproject_api.py"]
