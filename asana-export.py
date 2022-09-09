import asana

client = asana.Client.access_token('1/1201719304365594:39ca3917c86bb065b217dfe234e4731c')

result = client.projects.get_projects({'param': 'value', 'param': 'value'}, opt_pretty=True)
