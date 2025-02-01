use tokio::runtime::Runtime;
mod parser;
use parser::{clean_data, ScholarArticle};
use serde_json;

fn main() {
    let rt = Runtime::new().unwrap();
    rt.block_on(async {
        let raw_json = r#"
            [
                {
                    "title": "Reinforcement Learning for Smart Contracts",
                    "link": "https://scholar.google.com/example",
                    "snippet": "This paper explores RL in smart contract optimizations...",
                    "citation_info": "Cited by 32"
                },
                {
                    "title": "Blockchain Security with AI",
                    "link": "https://scholar.google.com/example2",
                    "snippet": "An overview of AI-based blockchain security...",
                    "citation_info": "Cited by 21"
                }
            ]
        "#;

        let articles: Vec<ScholarArticle> = serde_json::from_str(raw_json).unwrap();
        let cleaned_articles = clean_data(articles);

        println!("✅ Processed Articles:");
        for article in cleaned_articles {
            println!("{:?}", article);
        }
    });
}
