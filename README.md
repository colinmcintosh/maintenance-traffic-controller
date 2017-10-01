#### Created at the NANOG 71 Hackathon

# Maintenance Notification Traffic Controller

Created by Colin McIntosh & [...](#)


## Overview

This is a simple service that takes network links out of service based
on a schedule created from planned-maintenance notifications from
partners, carriers, and peers.

This is a continuation of a previous NANOG Hackathon project called
"Manage-Maintenance" which can be found here: https://github.com/colinmcintosh/manage-maintenance

The Manage-Maintenance service will read emails and populate the
schedule database. This service will periodically read from the schedule
database and take network links in & out of service at appropriate
times.
