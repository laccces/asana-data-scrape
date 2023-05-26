import asana

client = asana.Client.access_token('1/1201719304365594:93eb946e8425cb45865ad7829a527f0c')

result = client.projects.get_projects({'param': 'value', 'param': 'value'}, opt_pretty=True)
