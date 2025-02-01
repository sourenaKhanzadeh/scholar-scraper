use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use regex::Regex;

#[derive(Debug, Serialize, Deserialize)]
pub struct ScholarArticle {
    title: String,
    link: String,
    snippet: String,
    citation_info: String,
}

pub fn clean_data(articles: Vec<ScholarArticle>) -> Vec<ScholarArticle> {
    let citation_regex = Regex::new(r"Cited by (\d+)").unwrap();

    articles
        .into_par_iter()
        .map(|mut article| {
            article.snippet = article.snippet.trim().to_string();
            
            // Extract citation count
            if let Some(caps) = citation_regex.captures(&article.citation_info) {
                article.citation_info = format!("Cited by: {}", &caps[1]);
            }

            article
        })
        .collect()
}
