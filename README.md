#### Created at the NANOG 71 Hackathon

# Maintenance Notification Traffic Controller

Created by Colin McIntosh & [Aaron Atac](https://github.com/kopazetic)


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

## Notice Regarding Use in Production

Do not use this in production.

## License

MIT License

Copyright (c) 2017 Colin McIntosh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
