import twint

# Configure
c = twint.Config()
c.Search = "covid vaccin"
c.Lang = "fr"
c.Geo = "48.880048,2.385939,5km"
c.Limit = 300
c.Output = "./test.json"
c.Store_json = True

# Run
twint.run.Search(c)
