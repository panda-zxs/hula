# hula
---

The Hula project is a frontend and backend separated application built using Python Django and React. It aims to provide users with a comprehensive and powerful data analysis platform to showcase scientific analysis results.

The frontend of the Hula project is developed using the React framework, which is a popular JavaScript library focused on building user interfaces. With React, developers can create interactive and highly customizable data analysis interfaces to meet various needs. The component-based and virtual DOM technologies of React enable efficient construction of complex user interfaces and ensure fast data updates and responsiveness.

The backend of the project utilizes the Django framework, which is a robust and flexible Python web framework. Django offers rich features and tools that enable developers to quickly build efficient web applications. Its modular design and built-in database support simplify data storage and management. With Django, the Hula project can handle complex data processing logic and user authentication, providing users with a secure and reliable data analysis environment.

The core features of the Hula project lie in its rich data analysis capabilities and flexibility for customization. It provides various data processing and computation functionalities, including data cleaning, transformation, aggregation, statistics, and visualization. Users can leverage the tools and functions provided by Hula to perform diverse data analysis tasks according to their specific needs. Additionally, Hula supports custom formula and script writing, empowering users to define their own data processing logic and apply it to datasets.

In summary, the Hula project is a frontend and backend separated application utilizing React as the frontend technology and Django as the backend technology. It offers comprehensive and powerful data analysis functionalities to support scientific computation and data processing. With a wide range of tools and functions, Hula enables developers to quickly build and customize data analysis dashboards. Whether it's data cleaning, transformation, statistics, or visualization, Hula caters to users' needs. By supporting custom formula and script writing, Hula provides even higher flexibility and customization for data processing and analysis tasks.

---

### Usage
```python
from formula.parser import Parser
col = ['id', 'app_ym', 'Org', 'pro_label', 'target', 'sampwt', 'hit_rule',
           'appAge', 'appResidence', 'appTimeAddress', 'appIncome', 'appOcc',
           'appFinanceCo', 'appChkSv', 'dealNewUsed', 'dealLoanToVal', 'cbFICO',
           'cbTimeFile', 'cbMosAvg', 'cbUtilizn', 'cb90Ever', 'cbPctGood',
           'cbMosDlq', 'cbInq5Mos', 'cbMosInq', 'quickmodel_score']
df = pandas.read_csv("./AutoLoans.csv")
tokens, builder = Parser(df).ast("""
=if(app_ym<=201810, if(target, "kdsakdmak", "fsafafaf"), Org)
""")
d = builder.run()
print(d)

```