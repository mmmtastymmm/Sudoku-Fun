# This runs the GUI on docker for linux. Run from this directory.

# Make the container name
DOCKER_CONTAINER_NAME="sudoku-fun-run"
# Build the image
docker build -f run.Dockerfile -t mmmtastymmm/sudoku-fun-run:0.1.0 ..
# Run the image (it will error out without being added to xhosts)
docker run -it --name $DOCKER_CONTAINER_NAME \
  --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    mmmtastymmm/sudoku-fun-run:0.1.0

# Stop the image now, to get the id
docker stop $DOCKER_CONTAINER_NAME
CONTAINER_ID=$(docker ps -l -q)
# Add the id to the xhost (to let this run on the machine)
xhost +local:"$(docker inspect --format='{{ .Config.Hostname }}' ${CONTAINER_ID})"
# Now start that xhost can allow this to run
docker start $DOCKER_CONTAINER_NAME

# Now loop until the image closes
sleep 4s
while [ "$( docker container ls | grep ${DOCKER_CONTAINER_NAME} | wc -l )" -gt 0 ]; do
    sleep 4s
done

# The image has closed, so now can remove the xhost addition and the container
xhost -local:"$(docker inspect --format='{{ .Config.Hostname }}' ${CONTAINER_ID})"
docker rm $DOCKER_CONTAINER_NAME