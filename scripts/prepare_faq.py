from pathlib import Path
import pandas as pd
from faq_agent.data import load_faqs

df = pd.DataFrame(load_faqs(Path("data/faq.csv")))

full_df = pd.DataFrame(load_faqs(Path("data/faq-full.csv")))
