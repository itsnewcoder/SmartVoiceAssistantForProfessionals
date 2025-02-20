import streamlit as st
import speech_recognition as sr
import re
import datetime
import pandas as pd
import base64
from dateutil import parser
import time
import os

# Set page configuration
st.set_page_config(page_title="Voice-to-Action Assistant", page_icon="🎙️", layout="wide")

# Initialize session state variables
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'action_items' not in st.session_state:
    st.session_state.action_items = []
if 'meeting_details' not in st.session_state:
    st.session_state.meeting_details = {"date": None, "time": None, "duration": None}
if 'key_points' not in st.session_state:
    st.session_state.key_points = []

def record_audio():
    """Record audio from microphone and return the audio data"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        st.info("Listening... Speak now")
        audio = recognizer.listen(source, phrase_time_limit=30)
    return audio

def transcribe_audio(audio):
    """Transcribe audio to text using Google Speech Recognition"""
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio"
    except sr.RequestError:
        return "Could not request results from the speech recognition service"

def extract_action_items(text):
    """Extract action items from transcribed text - simplified version without NLTK"""
    # Split text into sentences using simple regex
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    action_items = []
    
    # Keywords that typically indicate action items
    action_keywords = ["need to", "should", "will", "must", "going to", "plan to", "have to", "task", "action item", "todo"]
    
    for sentence in sentences:
        # Check if sentence contains action verbs or keywords
        if any(keyword in sentence.lower() for keyword in action_keywords):
            # Extract deadline if present
            deadline_match = re.search(r'by\s(tomorrow|today|monday|tuesday|wednesday|thursday|friday|saturday|sunday|\d{1,2}(?:st|nd|rd|th)?\s(?:of\s)?(?:january|february|march|april|may|june|july|august|september|october|november|december)|(?:january|february|march|april|may|june|july|august|september|october|november|december)\s\d{1,2}(?:st|nd|rd|th)?|\d{1,2}/\d{1,2}(?:/\d{2,4})?)', sentence.lower())
            
            deadline = deadline_match.group(1) if deadline_match else "No deadline specified"
            
            action_items.append({
                "task": sentence,
                "deadline": deadline
            })
    
    return action_items

def extract_meeting_details(text):
    """Extract meeting details like date, time and duration"""
    meeting_details = {"date": None, "time": None, "duration": None}
    
    # Try to find date
    date_patterns = [
        r'(?:on\s)?(today|tomorrow|(?:next\s)?(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday))',
        r'(?:on\s)?(\d{1,2}(?:st|nd|rd|th)?\s(?:of\s)?(?:january|february|march|april|may|june|july|august|september|october|november|december))',
        r'(?:on\s)?(\d{1,2}/\d{1,2}(?:/\d{2,4})?)'
    ]
    
    for pattern in date_patterns:
        date_match = re.search(pattern, text.lower())
        if date_match:
            meeting_details["date"] = date_match.group(1)
            break
    
    # Try to find time
    time_match = re.search(r'(?:at\s)?(\d{1,2}(?::\d{2})?\s?(?:am|pm))', text.lower())
    if time_match:
        meeting_details["time"] = time_match.group(1)
    
    # Try to find duration
    duration_match = re.search(r'(?:for\s)?(\d+\s?(?:hour|minute)s?)', text.lower())
    if duration_match:
        meeting_details["duration"] = duration_match.group(1)
    
    return meeting_details

def extract_key_points(text):
    """Extract key discussion points from transcribed text - simplified version without NLTK"""
    # Split text into sentences using simple regex
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    key_points = []
    
    importance_keywords = [
        "important", "significant", "key", "critical", "essential", "main point",
        "highlight", "crucial", "major", "primary", "fundamental"
    ]
    
    for sentence in sentences:
        # Check if sentence contains importance indicators
        if any(keyword in sentence.lower() for keyword in importance_keywords):
            key_points.append(sentence)
        
        # Also check for statements that sound like conclusions or agreements
        elif any(word in sentence.lower() for word in ["agree", "conclusion", "decided", "consensus", "summary"]):
            key_points.append(sentence)
    
    # If no key points found with keywords, use the first sentence and other sentences that appear important
    if not key_points and sentences:
        key_points.append(sentences[0])
        
        # Check for sentences that appear to be important (contains nouns, longer sentences, etc.)
        for sentence in sentences[1:]:
            # Simple heuristic: longer sentences with proper capitalization might be important points
            if len(sentence.split()) > 8 and any(word[0].isupper() for word in sentence.split()):
                key_points.append(sentence)
    
    return key_points[:5]  # Limit to top 5 key points

def generate_calendar_event(meeting_details):
    """Generate iCalendar format for extracted meeting details"""
    if not meeting_details["date"] or not meeting_details["time"]:
        return None
    
    try:
        # Try to parse the date and time
        meeting_date_str = meeting_details["date"]
        meeting_time_str = meeting_details["time"]
        
        # Handle relative dates
        if meeting_date_str.lower() == "today":
            meeting_date = datetime.date.today()
        elif meeting_date_str.lower() == "tomorrow":
            meeting_date = datetime.date.today() + datetime.timedelta(days=1)
        else:
            try:
                # Try to parse the complete date
                meeting_datetime = parser.parse(f"{meeting_date_str} {meeting_time_str}")
                return meeting_datetime.strftime("%Y-%m-%d %H:%M")
            except:
                return None
        
        # Combine with time
        try:
            meeting_time = parser.parse(meeting_time_str).time()
            meeting_datetime = datetime.datetime.combine(meeting_date, meeting_time)
            return meeting_datetime.strftime("%Y-%m-%d %H:%M")
        except:
            return None
            
    except:
        return None

def generate_todo_list(action_items):
    """Generate a formatted todo list from action items"""
    if not action_items:
        return "No action items identified."
    
    todo_list = []
    for item in action_items:
        deadline_text = f" (Due: {item['deadline']})" if item['deadline'] != "No deadline specified" else ""
        todo_list.append(f"- {item['task']}{deadline_text}")
    
    return "\n".join(todo_list)

def generate_meeting_summary(transcribed_text, key_points, action_items, meeting_details):
    """Generate a meeting summary from extracted information"""
    summary = "# Meeting Summary\n\n"
    
    # Add meeting details if available
    if meeting_details["date"] or meeting_details["time"]:
        summary += "## Meeting Details\n"
        if meeting_details["date"]:
            summary += f"- Date: {meeting_details['date']}\n"
        if meeting_details["time"]:
            summary += f"- Time: {meeting_details['time']}\n"
        if meeting_details["duration"]:
            summary += f"- Duration: {meeting_details['duration']}\n"
        summary += "\n"
    
    # Add key points
    if key_points:
        summary += "## Key Discussion Points\n"
        for i, point in enumerate(key_points, 1):
            summary += f"{i}. {point}\n"
        summary += "\n"
    
    # Add action items
    if action_items:
        summary += "## Action Items\n"
        for i, item in enumerate(action_items, 1):
            deadline = f" (Due: {item['deadline']})" if item['deadline'] != "No deadline specified" else ""
            summary += f"{i}. {item['task']}{deadline}\n"
        summary += "\n"
    
    # Add full transcript
    summary += "## Full Transcript\n"
    summary += transcribed_text
    
    return summary

def get_download_link(text, filename, label="Download"):
    """Generate a download link for text content"""
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{label}</a>'
    return href

# App Layout
st.title("🎙️ Voice-to-Action Assistant")
st.subheader("Smart meeting assistant for professionals")

tabs = st.tabs(["Record", "Process & Extract", "Generate Actions", "Summary"])

# Tab 1: Record
with tabs[0]:
    st.markdown("### Record Meeting Audio")
    st.write("Click the button below to start recording. Speak clearly for best results.")
    
    col1, col2 = st.columns(2)
    
    if col1.button("🎙️ Start Recording"):
        st.session_state.recording = True
        with st.spinner("Recording..."):
            audio_data = record_audio()
            st.write("Transcribing audio...")
            text = transcribe_audio(audio_data)
            st.session_state.transcribed_text += text + " "
            st.session_state.recording = False
    
    if col2.button("⏹️ Stop Recording"):
        st.session_state.recording = False
    
    if st.session_state.recording:
        st.warning("Recording in progress...")
    
    st.markdown("### Current Transcript")
    transcript_area = st.text_area("Edit transcript if needed", value=st.session_state.transcribed_text, height=300)
    st.session_state.transcribed_text = transcript_area
    
    if st.button("Clear Transcript"):
        st.session_state.transcribed_text = ""
        st.experimental_rerun()

# Tab 2: Process & Extract
with tabs[1]:
    st.markdown("### Process Transcript & Extract Information")
    
    if st.button("🔍 Process Transcript"):
        if st.session_state.transcribed_text:
            with st.spinner("Processing transcript..."):
                # Extract action items
                st.session_state.action_items = extract_action_items(st.session_state.transcribed_text)
                
                # Extract meeting details
                st.session_state.meeting_details = extract_meeting_details(st.session_state.transcribed_text)
                
                # Extract key points
                st.session_state.key_points = extract_key_points(st.session_state.transcribed_text)
                
                st.success("Processing complete!")
        else:
            st.error("Please record or enter a transcript first.")
    
    st.markdown("### Extracted Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Action Items")
        if st.session_state.action_items:
            for i, item in enumerate(st.session_state.action_items, 1):
                st.write(f"{i}. {item['task']}")
                st.caption(f"Deadline: {item['deadline']}")
        else:
            st.info("No action items extracted yet.")
    
    with col2:
        st.subheader("Meeting Details")
        if st.session_state.meeting_details:
            details = st.session_state.meeting_details
            if details["date"]:
                st.write(f"📅 Date: {details['date']}")
            if details["time"]:
                st.write(f"🕒 Time: {details['time']}")
            if details["duration"]:
                st.write(f"⏱️ Duration: {details['duration']}")
            if not details["date"] and not details["time"] and not details["duration"]:
                st.info("No meeting details extracted.")
        
        st.subheader("Key Discussion Points")
        if st.session_state.key_points:
            for i, point in enumerate(st.session_state.key_points, 1):
                st.write(f"{i}. {point}")
        else:
            st.info("No key points extracted yet.")

# Tab 3: Generate Actions
with tabs[2]:
    st.markdown("### Generate Digital Actions")
    
    calendar_col, todo_col = st.columns(2)
    
    with calendar_col:
        st.subheader("📅 Calendar Event")
        calendar_event_time = generate_calendar_event(st.session_state.meeting_details)
        
        if calendar_event_time:
            st.success(f"Meeting scheduled for: {calendar_event_time}")
            
            event_title = st.text_input("Event Title", "Meeting")
            event_location = st.text_input("Location", "")
            
            if st.button("Add to Calendar"):
                st.success("Calendar event created!")
                # In a real app, this would integrate with calendar APIs
                st.code(f"""
                Event: {event_title}
                Date/Time: {calendar_event_time}
                Location: {event_location}
                """)
        else:
            st.info("Meeting details insufficient to create calendar event.")
    
    with todo_col:
        st.subheader("✅ Todo List")
        todo_list = generate_todo_list(st.session_state.action_items)
        
        if todo_list != "No action items identified.":
            st.markdown(todo_list)
            
            if st.button("Export Todo List"):
                todo_text = "# Todo List\n\n" + todo_list
                st.markdown(get_download_link(todo_text, "todo_list.txt", "📥 Download Todo List"), unsafe_allow_html=True)
        else:
            st.info("No action items to create todos.")
    
    st.subheader("📧 Share Key Points")
    if st.session_state.key_points:
        recipient = st.text_input("Recipient Email")
        subject = st.text_input("Subject", "Meeting Key Points")
        
        email_content = "# Key Points from Meeting\n\n"
        for i, point in enumerate(st.session_state.key_points, 1):
            email_content += f"{i}. {point}\n"
        
        st.text_area("Email Content", email_content, height=200)
        
        if st.button("Send Email"):
            if recipient:
                st.success(f"Email sent to {recipient}!")
                # In a real app, this would integrate with email APIs
            else:
                st.error("Please enter a recipient email.")
    else:
        st.info("No key points to share. Process the transcript first.")

# Tab 4: Summary
with tabs[3]:
    st.markdown("### Meeting Summary")
    
    if st.button("Generate Complete Summary"):
        if st.session_state.transcribed_text:
            with st.spinner("Generating summary..."):
                summary = generate_meeting_summary(
                    st.session_state.transcribed_text,
                    st.session_state.key_points,
                    st.session_state.action_items,
                    st.session_state.meeting_details
                )
                st.markdown(summary)
                st.markdown(get_download_link(summary, "meeting_summary.md", "📥 Download Summary"), unsafe_allow_html=True)
        else:
            st.error("Please record or enter a transcript first.")
    
    st.markdown("### Save All Data")
    if st.button("Export All Data"):
        if st.session_state.transcribed_text:
            # Create a comprehensive export
            export_data = {
                "transcript": st.session_state.transcribed_text,
                "action_items": st.session_state.action_items,
                "meeting_details": st.session_state.meeting_details,
                "key_points": st.session_state.key_points
            }
            
            # Convert to JSON string
            import json
            export_json = json.dumps(export_data, indent=4)
            
            st.markdown(get_download_link(export_json, "meeting_data.json", "📥 Download All Data (JSON)"), unsafe_allow_html=True)
        else:
            st.error("No data to export. Please record or enter a transcript first.")

# Footer
st.markdown("---")
st.caption("Voice-to-Action Assistant | Prototype Version")