import streamlit as st

def styles_main():
   element_style = '''<style>
   #root > div:nth-child(1) > div.withScreencast > div > div > header{
   display: none}
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5{
   padding:0 !important;
   }
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(5),
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6){
   display: none
   }
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5{
   margin:0 20vw
   }
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div{
   gap:0 !important;}

   /* pading en dropdown genres */
   #complexnavbarSupportedContent ul li a {
      padding: 2px 1rem !important;
   }

   /*widht max */
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5{
   max-width: 100vw !important}

   /* gap */
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div{
   gap:0 !important}

   /*  margin beetwen selected and posters */
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(12) > div > div > div{
   margin-bottom:10px}
    </style>
   '''
   st.markdown(element_style, unsafe_allow_html=True)   