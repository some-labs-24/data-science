# Put commonly used  command line commands here for reference.

## Docker - Build docker image:

```docker build -t myimage .```

This will start to build a docker image, including downloading any pip installations and whatever else is specified in ```Dockerfile```. You'll have to do this every time you make changes, followed by the run command below.

## Docker - Run docker image locally:

```docker run -d --name mycontainer -p 80:80 myimage```

Then go to Docker dashboard, go to your list of containers, and click "open in browser".

## Elastic Beanstalk - Initialize app:

```eb init -p docker So-Me-DS-API```

This will create a .elasticbeanstalk file. You should only have to do this once. If you have not already, you will have to connect your EB CLI to your AWS account when you do this. 

## Elastic Beanstalk - Create new environment

```eb create So-Me-FastAPI```

This will create an entire new Elastic Beanstalk environment on AWS. You should do this if you're starting from scratch, otherwise, use the following to deploy to an existing environment:

## Elastic Beanstalk - Deploy to existing environment

```eb deploy So-Me-FastAPI```