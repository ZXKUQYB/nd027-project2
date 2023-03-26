# Project: Data Modeling with Apache Cassandra

<br>

This project is considered as an extension of the Project: Data Modeling with Postgres, the 1st project of the Data Engineering Nanodegree program. It shares the same purpose and analytical goals in context of the company Sparkify, as well as the design of database schemas, but with the following differences in ETL pipelines:

* The main database system used in the project is [Apache Cassandra](https://cassandra.apache.org/), a NoSQL database management system developed by Apache Software Foundation. Since it is not a SQL database anymore, Cassandra uses its own language, [CQL](https://cassandra.apache.org/doc/latest/cassandra/cql/), to manipulate data. It is similar to SQL, but do not expect CQL to be functionally compatible to all the SQL queries we know.
* The unprocessed JSON raw files are not available in this project. Instead, they have been combined into unprocessed CSV files (raw entries aggregated by date and saved in separate files) to serve as the raw dataset. It seems that Cassandra is also capable of handling JSON files to some extent (see [this](https://stackoverflow.com/questions/40389690/importing-json-dataset-into-cassandra) or [this](https://docs.datastax.com/en/cql-oss/3.3/cql/cql_using/useInsertJSON.html) for some examples), but these prepared CSV files are much easier to use in this project.

<br>

NoSQL databases are designed to scale horizontally better than traditional SQL databases, but (in most cases) with the price of sacrificing ACID compliance. This is also true to Apache Cassandra. [Case studies](https://cassandra.apache.org/_/case-studies.html) showed that most of the Cassandra use cases are dealing with extreme amount of data (eg. hundreds of terabytes or petabytes). Actually many SQL databases usually have features like partitioned tables that are suitable in such cases, but these features come with some limitations imposed by the software itself. Following is a list of general SQL databases and their maximum partitions allowed per table:

* MySQL : 1024 ([5.6 and before](https://arctype.com/blog/mysql-partitions/)) or 8192 ([5.7 and above](https://dev.mysql.com/doc/refman/5.7/en/partitioning-limitations.html))
* Microsoft SQL Server : 1000 (before SQL Server 2012) or 15000 (see [here](https://learn.microsoft.com/en-us/sql/relational-databases/partitions/partitioned-tables-and-indexes?view=sql-server-ver16) for more info)
* Oracle Database : 65535 (in [9iR2](https://docs.oracle.com/cd/B10500_01/server.920/a96536/ch44.htm#288033) and [10gR1](https://docs.oracle.com/cd/B14117_01/server.101/b10755/limits003.htm#i288032)) or 1048575 (in [10gR2](https://docs.oracle.com/cd/B19306_01/server.102/b14237/limits003.htm#i288032) and [above](https://docs.oracle.com/en/database/oracle/oracle-database/index.html))
* PostgreSQL : According to the [official online docs](https://www.postgresql.org/docs/current/limits.html), it seems that there is no hard limit related to number of partitions per table defined in PostgreSQL (Whoa!), except the resource limit of the machine running PostgreSQL software. There are also some database folks attempting to test the limits of number of partitions like [this](https://elephas.io/is-there-a-limit-on-number-of-partitions-handled-by-postgres/) and [this](https://www.depesz.com/2021/01/17/are-there-limits-to-partition-counts/), indicating that the PostgreSQL software version may also be a key factor in table partitioning.

Also, remember that partitioned tables are considered as a practice of vertical scaling, which means huge amounts of data are stored in a single machine. That's not the horizontal scaling we can expect when using NoSQL databases like Apache Cassandra. For SQL databases to do the same thing, the best bet we can expect would be some sorts of database clustering (or clustering-like, at least) solutions, such as 

- Oracle's [RAC](https://www.oracle.com/database/real-application-clusters/)
- Microsoft's [Always On](https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/overview-of-always-on-availability-groups-sql-server?view=sql-server-ver16)
- MySQL's [Cluster CGE](https://www.mysql.com/products/cluster/)
- PostgreSQL's [Foreign data wrappers](https://www.postgresql.org/docs/current/postgres-fdw.html) (do not confuse the PostgreSQL's built-in CLUSTER command with these solutions, see [here](https://www.opsdash.com/blog/postgresql-cluster.html) for more info)

And of course, these clustering solutions come with limits of maximum number of nodes. Meanwhile, take a look at [Apple](https://twitter.com/pauloricardomg/status/510198452345528321) - they were running their own on-premises Cassandra installations composed of more than 75000 nodes in 2014 already. So if you are looking for some serious scalability, Cassandra is an option that could be considered.

<br>

There is no standalone Python script in this project, only a Jupyter Notebook file available. It is intended to serve as a proof of concept, demonstrating how it feels like to carry out the same task we accomplished earlier in the previous project, but using Cassandra to substitute for PostgreSQL.
