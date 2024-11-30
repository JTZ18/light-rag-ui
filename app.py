import streamlit as st
from query import rag, QueryParam
import pandas as pd

st.title("LightRAG Query Interface")

# Query mode selection
query_mode = st.selectbox(
    "Select Query Mode",
    ["hybrid", "naive", "local", "global"],
    index=0
)

# Query input
query = st.text_input("Enter your query")

if query:
    # Get context and answer
    context = rag.query(query, param=QueryParam(mode=query_mode, only_need_context=True))
    answer = rag.query(query, param=QueryParam(mode=query_mode, only_need_context=False))

    # Display answer
    st.header("Generated Answer")
    st.write(answer)

    # Display context
    st.header("Source Context")

    # Parse and display context sections in expandable sections
    if "-----Entities-----" in context:
        with st.expander("Entities", expanded=False):
            # Extract entities section
            entities_text = context.split("-----Entities-----")[1].split("-----Relationships-----")[0]

            try:
                # Convert CSV string to DataFrame
                entities_df = pd.read_csv(pd.StringIO(entities_text))
                st.dataframe(entities_df)
            except:
                st.text(entities_text)

    if "-----Relationships-----" in context:
        with st.expander("Relationships", expanded=False):
            # Extract relationships section
            relationships_text = context.split("-----Relationships-----")[1].split("-----Sources-----")[0]

            try:
                # Convert CSV string to DataFrame
                relationships_df = pd.read_csv(pd.StringIO(relationships_text))
                st.dataframe(relationships_df)
            except:
                st.text(relationships_text)

    if "-----Sources-----" in context:
        with st.expander("Sources", expanded=False):
            # Extract sources section
            sources_text = context.split("-----Sources-----")[1]

            try:
                # Convert CSV string to DataFrame
                sources_df = pd.read_csv(pd.StringIO(sources_text))
                st.dataframe(sources_df)
            except:
                st.text(sources_text)