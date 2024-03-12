FROM condaforge/miniforge3:latest
COPY app /app
RUN conda env create -f /app/environment.yml
ENTRYPOINT ["/opt/conda/envs/reproject/bin/python"]
CMD ["/app/reproject_api.py"]
