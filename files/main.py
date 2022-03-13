#!/usr/bin/env python3

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import securitycenter
import google.auth
from google.cloud import logging

client = securitycenter.SecurityCenterClient()
logging_client = logging.Client()


def scc_helper_updated(request):
    request_json = request.get_json(silent=True)
    request_args = request.args
    message = {}
    # Checking compliance
    if request_json and "compliance" in request_json:
        compliance = str(request_json["compliance"])
        comp_status = True
    elif request_args and "compliance" in request_args:
        compliance = str(request_args["compliance"])
        comp_status = True
    else:
        comp_status = False
        compliance = ""

    if request_json and "critical_max" in request_json:
        critical_max = int(float(request_json["critical_max"]))

    elif request_args and "critical_max" in request_args:
        critical_max = int(float(request_args["critical_max"]))

    else:
        print("Using zero as critical max value")
        critical_max = 0

    if request_json and "scoped_project" in request_json:
        project_id = request_json["scoped_project"]

    elif request_args and "scoped_project" in request_args:
        project_id = request_args["scoped_project"]

    else:
        print("Using Cloud Function Project ID as scoped_project")
        credentials, project_id = google.auth.default()

    if request_json and "high_max" in request_json:
        high_max = int(float(request_json["high_max"]))

    elif request_args and "high_max" in request_args:
        high_max = int(float(request_args["high_max"]))

    else:
        print("Using zero as high max value")
        high_max = 0

    if request_json and "medium_max" in request_json:
        medium_max = int(float(request_json["medium_max"]))

    elif request_args and "medium_max" in request_args:
        medium_max = int(float(request_args["medium_max"]))

    else:
        print("Using zero as Medium max value")
        medium_max = 0

    if request_json and "logger_name" in request_json:
        logger_name = str(request_json["logger_name"])

    elif request_args and "logger_name" in request_args:
        logger_name = str(request_args["logger_name"])
    else:
        print("Using logger name: scc_logging")
        logger_name = "scc_logging"

    logger = logging_client.logger(logger_name)

    # credentials, project_id = google.auth.default()

    project_name = "projects/{project_id}".format(project_id=project_id)

    # The "sources/-" suffix lists findings across all sources.  You
    # also use a specific source_name instead.
    source_name = "{project_name}/sources/-".format(project_name=project_name)
    standard = "source_properties.compliance_standards"
    filter_hcm = "severity=\"HIGH\" OR severity=\"CRITICAL\" \
        OR severity=\"MEDIUM\""
    filter_critical = "state=\"ACTIVE\" AND (severity=\"CRITICAL\")"
    filter_high = "state=\"ACTIVE\" AND (severity=\"HIGH\")"
    filter_med = "state=\"ACTIVE\" AND (severity=\"MEDIUM\")"

    if comp_status is False:

        FILTER = "state=\"ACTIVE\" AND ({})".format(filter_hcm)

        finding_result_iterator = client.list_findings(
            request={"parent": source_name, "filter": FILTER})

        # Get Total Findings
        total_findings = finding_result_iterator.total_size

        # Get total critical findings
        FILTER = "state=\"ACTIVE\" AND (severity=\"CRITICAL\")"
        critical_finding_result_iterator = client.list_findings(
            request={"parent": source_name, "filter": FILTER})
        critical_findings = critical_finding_result_iterator.total_size
        # Get total high findings
        FILTER = "state=\"ACTIVE\" AND (severity=\"HIGH\")"
        high_finding_result_iterator = client.list_findings(
            request={"parent": source_name, "filter": FILTER})
        high_findings = high_finding_result_iterator.total_size

        # Get total medium findings
        FILTER = "state=\"ACTIVE\" AND (severity=\"MEDIUM\")"
        medium_finding_result_iterator = client.list_findings(
            request={"parent": source_name, "filter": FILTER})
        medium_findings = medium_finding_result_iterator.total_size
    else:
        if compliance == "iso":
            FILTER = "state=\"ACTIVE\" AND ({}) AND ({} :\"iso\")".format(
                filter_hcm, standard)
        elif compliance == "nist":
            FILTER = "state=\"ACTIVE\" AND ({}) AND ({} :\"nist\")".format(
                filter_hcm, standard)
        elif compliance == "cis":
            FILTER = "state=\"ACTIVE\" AND ({}) AND ({} :\"cis\")".format(
                filter_hcm, standard)
        elif compliance == "pci":
            FILTER = "state=\"ACTIVE\" AND ({}) AND ({} :\"pci\")".format(
                filter_hcm, standard)

        # Get Total Findings
        finding_result_iterator = client.list_findings(
            request={"parent": source_name, "filter": FILTER})
        total_findings = finding_result_iterator.total_size

        if compliance == "iso":
            FILTER = "{} AND ({} :\"iso\")".format(filter_critical, standard)
        elif compliance == "nist":
            FILTER = "{} AND ({} :\"nist\")".format(filter_critical, standard)
        elif compliance == "cis":
            FILTER = "{} AND ({} :\"cis\")".format(filter_critical, standard)
        elif compliance == "pci":
            FILTER = "{} AND ({} :\"pci\")".format(filter_critical, standard)

        # Get total critical findings
        critical_finding_result_iterator = client.list_findings(
            request={"parent": source_name, "filter": FILTER})
        critical_findings = critical_finding_result_iterator.total_size

        # Get total high findings
        if compliance == "iso":
            FILTER = "{} AND ({} :\"iso\")".format(filter_high, standard)
        elif compliance == "nist":
            FILTER = "{} AND ({} :\"nist\")".format(filter_high, standard)
        elif compliance == "cis":
            FILTER = "{} AND ({} :\"cis\")".format(filter_high, standard)
        elif compliance == "pci":
            FILTER = "{} AND ({} :\"pci\")".format(filter_high, standard)

        high_finding_result_iterator = client.list_findings(
            request={"parent": source_name, "filter": FILTER})
        high_findings = high_finding_result_iterator.total_size

        # Get total Medium findings
        if compliance == "iso":
            FILTER = "{} AND ({} :\"iso\")".format(filter_med, standard)
        elif compliance == "nist":
            FILTER = "{} AND ({} :\"nist\")".format(filter_med, standard)
        elif compliance == "cis":
            FILTER = "{} AND ({} :\"cis\")".format(filter_med, standard)
        elif compliance == "pci":
            FILTER = "{} AND ({} :\"pci\")".format(filter_med, standard)

        medium_finding_result_iterator = client.list_findings(
            request={"parent": source_name, "filter": FILTER})
        medium_findings = medium_finding_result_iterator.total_size

    if high_findings > high_max or critical_findings > critical_max or medium_findings > medium_max:

        if critical_findings > 0:
            print(
                '\x1b[6;30;42m' +
                'CRITICAL SEVERITY FINDINGS!' +
                '\x1b[0m' +
                '\n')
            for i, finding_result in enumerate(
                    critical_finding_result_iterator):
                print(
                    "Name: {}\n Category: {}\n \
                        Resource: {}\n URI: {}\n".format(
                        finding_result.finding.name,
                        finding_result.finding.category,
                        finding_result.finding.resource_name,
                        finding_result.finding.external_uri))
                dict = {
                    "Name": finding_result.finding.name,
                    "Category": finding_result.finding.category,
                    "Resource": finding_result.finding.resource_name,
                    "URI": finding_result.finding.external_uri}
                message["key"] = dict
                write_entry(logger_name, message["key"])
        if high_findings > 0:
            print(
                '\x1b[6;30;42m' +
                'HIGH SEVERITY FINDINGS!' +
                '\x1b[0m' +
                '\n')
            for i, finding_result in enumerate(high_finding_result_iterator):
                print(
                    "Name: {}\n Category: {}\n \
                        Resource: {}\n URI: {}\n".format(
                        finding_result.finding.name,
                        finding_result.finding.category,
                        finding_result.finding.resource_name,
                        finding_result.finding.external_uri))
                dict = {
                    "Name": finding_result.finding.name,
                    "Category": finding_result.finding.category,
                    "Resource": finding_result.finding.resource_name,
                    "URI": finding_result.finding.external_uri}
                message["key"] = dict
                write_entry(logger_name, message["key"])

        if medium_findings > 0:
            print(
                '\x1b[6;30;42m' +
                'MEDIUM SEVERITY FINDINGS!' +
                '\x1b[0m' +
                '\n')
            for i, finding_result in enumerate(medium_finding_result_iterator):
                print(
                    "Name: {}\n Category: {}\n \
                        Resource: {}\n URI: {}\n".format(
                        finding_result.finding.name,
                        finding_result.finding.category,
                        finding_result.finding.resource_name,
                        finding_result.finding.external_uri))
                dict = {
                    "Name": finding_result.finding.name,
                    "Category": finding_result.finding.category,
                    "Resource": finding_result.finding.resource_name,
                    "URI": finding_result.finding.external_uri}
                message["key"] = dict
                write_entry(logger_name, message["key"])

    print(
        "Total Finding: {} Critical : {} High : {} Medium : {} ".format(
            total_findings,
            critical_findings,
            high_findings,
            medium_findings))

    if (high_findings > high_max) or (critical_findings >
                                      critical_max) or (medium_findings > medium_max):

        print(
            '\x1b[6;30;42m' +
            'Build failed! Finding exceed max allowed ' +
            '\x1b[0m')
        logger.log_text(
            "Build failed! Finding exceed max allowed \n Total  Findings: ",
            severity="ERROR")
        logger.log_text(
            str(total_findings) +
            " Critical Findings: " +
            str(critical_findings) +
            " High Findings: " +
            str(high_findings) +
            " Medium Findings: " +
            str(medium_findings),
            severity="ERROR")
        raise RuntimeError('Build failed!')

    else:
        print(
            '\x1b[6;30;42m' +
            'Build passed for threshold provided!' +
            '\x1b[0m')
        logger.log_text("Build passed or threshold provided!", severity="INFO")
        logger.log_text(
            str(total_findings) +
            " Critical Findings: " +
            str(critical_findings) +
            " High Findings: " +
            str(high_findings) +
            " Medium Findings: " +
            str(medium_findings),
            severity="INFO")


def write_entry(logger_name, message):
    """Writes log entries to the given logger."""
    logging_client = logging.Client()

    # This log can be found in the Cloud Logging console under 'Custom Logs'.
    logger = logging_client.logger(logger_name)

    logger.log_struct(
        message, severity="INFO"
    )
