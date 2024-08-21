# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class MyprojectPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        # Fields that need to be converted to integers
        integer_fields = ['university_id', 'quota', 'status']

        for field in integer_fields:
            value = adapter.get(field)
            if value is not None:
                try:
                    # Convert the field value to an integer
                    adapter[field] = int(value.replace(',', '').strip())
                except ValueError:
                    # Handle cases where conversion fails, you can log a warning or set to None
                    spider.logger.warning(f"Could not convert {field} value '{value}' to int")
                    adapter[field] = None

        return item
class SaveToMySQLPipeline:
    def open_spider(self, spider):
        # Establish connection to the MySQL database
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='oy159753',
            database='yok_atlas'
        )
        self.cursor = self.conn.cursor()

        # Create table if it does not exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS your_table_name (
                university_id INT NOT NULL,
                university_name VARCHAR(255),
                faculty_name VARCHAR(255),
                department_name VARCHAR(255),
                language_and_program_type VARCHAR(255),
                location VARCHAR(255),
                university_type VARCHAR(255),
                fee_status VARCHAR(255),
                education_type VARCHAR(255),
                quota INT,
                status INT,
                PRIMARY KEY (university_id)
            )
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Construct the SQL query to insert the data
        sql = """
            INSERT INTO your_table_name (
                university_id, 
                university_name, 
                faculty_name, 
                department_name, 
                language_and_program_type, 
                location, 
                university_type, 
                fee_status, 
                education_type, 
                quota, 
                status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            adapter.get('university_id'),
            adapter.get('university_name'),
            adapter.get('faculty_name'),
            adapter.get('department_name'),
            adapter.get('language_and_program_type'),
            adapter.get('location'),
            adapter.get('university_type'),
            adapter.get('fee_status'),
            adapter.get('education_type'),
            adapter.get('quota'),
            adapter.get('status'),
        )
        
        # Execute the query
        self.cursor.execute(sql, values)
        self.conn.commit()

        return item
    
    def close_spider(self, spider):
        # Close the connection to the database when the spider is closed
        self.conn.commit()
        self.cursor.close()
        self.conn.close()