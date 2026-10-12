from get_another_incidents import get_another

def search_incident(incidents: list):
    for incident in incidents:
        dict_requirement_params = {}
        for key, value in incident.items():
            # TODO сборка dict_requirement_params исходя из выбранных правилом/дефолтных зн-ий key, value
            get_another(dict_requirement_params)










