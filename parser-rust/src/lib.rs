use mongodb::{bson::doc, Client, Collection};
use pyo3::prelude::*;  // ✅ Ensure PyO3 is included
use serde::{Deserialize, Serialize};
use tokio;

#[derive(Debug, Serialize, Deserialize)]
pub struct ScholarArticle {
    title: String,
    link: String,
    snippet: String,
    citation_info: String,
}

#[pyfunction]
fn save_to_mongo(json_data: &str) -> PyResult<String> {
    let rt = tokio::runtime::Runtime::new().unwrap();  // ✅ Fix async runtime issue
    rt.block_on(async {
        let client = Client::with_uri_str("mongodb://localhost:27017").await.unwrap();
        let db = client.database("scholar_db");
        let collection: Collection<ScholarArticle> = db.collection("articles");

        let articles: Vec<ScholarArticle> = serde_json::from_str(json_data).unwrap();
        collection.insert_many(articles, None).await.unwrap();
    });

    Ok("✅ Data saved successfully".to_string())
}

#[pymodule]
fn parser_rust(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(save_to_mongo, m)?)?;
    Ok(())
}
