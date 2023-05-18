# Job Tracking CLI Application

This is a CLI application that allows users to search for available jobs and keep track of the jobs they are applying to. The CLI app is built with Python, Rich, and PrettyTable. The database in built with SQLite3, SQLAlchemy, and Alembic.

## Installation

Clone this repo and run the following commands to set up the dependencies:

```console
$ cd job_tracking_app
$ pipenv install && pipenv shell
```

Run `bin/run`  to start the app:
```console
$ python bin/run
```

***

### Users
After starting the app, a new user will be prompted to add onself to the database while an existing user will be prompted to enter their information to retrieve the current active job applications the app is tracking.

The user has the option to view and filter the jobs in the database, add/delete a job application, view and sort their own active applications, and update the application status to keep track of the important milestones.

### Admin
The admin manages the databases so the admin not only can view all the available jobs, but also can view/delete the active users and edit/delete a job posting.

### Contributing

Bug reports and pull requests are welcome on GitHub at http:// ...

***
