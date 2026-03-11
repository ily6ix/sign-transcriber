"""
Export utilities for Sign Language Transcripts
Supports exporting to PDF, CSV, and TXT formats
"""
import csv
from io import StringIO, BytesIO
from datetime import datetime
from fpdf import FPDF
from typing import Dict, Tuple


class TranscriptExporter:
    """Handle transcript exports in multiple formats"""
    
    @staticmethod
    def export_txt(transcript) -> Tuple[str, str]:
        """
        Export transcript as plain text
        
        Args:
            transcript: Transcript model instance
            
        Returns:
            Tuple of (filename, content)
        """
        filename = f"{transcript.title.replace(' ', '_')}_{transcript.id}.txt"
        
        content = f"""TRANSCRIPT: {transcript.title}
{'='*60}

Created: {transcript.created_at.strftime('%B %d, %Y at %H:%M %p')}
Updated: {transcript.updated_at.strftime('%B %d, %Y at %H:%M %p')}
Status: {transcript.status.upper()}

{'─'*60}

{transcript.content}

{'─'*60}
End of Transcript
"""
        
        return filename, content
    
    @staticmethod
    def export_csv(transcript) -> Tuple[str, bytes]:
        """
        Export transcript as CSV with readable rows
        
        Args:
            transcript: Transcript model instance
            
        Returns:
            Tuple of (filename, csv_bytes)
        """
        filename = f"{transcript.title.replace(' ', '_')}_{transcript.id}.csv"
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Header information
        writer.writerow(["Transcript: " + transcript.title])
        writer.writerow([])
        writer.writerow(["Created:", transcript.created_at.strftime('%B %d, %Y at %H:%M %p')])
        writer.writerow(["Updated:", transcript.updated_at.strftime('%B %d, %Y at %H:%M %p')])
        writer.writerow(["Status:", transcript.status.upper()])
        if transcript.session_duration:
            writer.writerow(["Duration:", f"{transcript.session_duration} seconds"])
        writer.writerow([])
        
        # Content section
        writer.writerow(["CONTENT"])
        writer.writerow([])
        
        # Write content as words (one per row)
        if transcript.content:
            words = transcript.content.split()
            for word in words:
                writer.writerow([word])
        
        # Additional metadata if available
        if transcript.raw_content:
            writer.writerow([])
            writer.writerow(["DETECTED SIGNS (Raw)"])
            writer.writerow([])
            
            if isinstance(transcript.raw_content, list):
                for i, sign in enumerate(transcript.raw_content, 1):
                    writer.writerow([f"{i}. {sign}"])
            elif isinstance(transcript.raw_content, dict):
                for key, value in transcript.raw_content.items():
                    writer.writerow([f"{key}: {value}"])
        
        return filename, output.getvalue().encode('utf-8')
    
    @staticmethod
    def export_pdf(transcript) -> Tuple[str, bytes]:
        """
        Export transcript as formatted PDF
        
        Args:
            transcript: Transcript model instance
            
        Returns:
            Tuple of (filename, pdf_bytes)
        """
        filename = f"{transcript.title.replace(' ', '_')}_{transcript.id}.pdf"
        
        pdf = FPDF()
        pdf.add_page()
        
        # Set fonts
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 15, f"Transcript: {transcript.title}", ln=True, align="C")
        
        # Horizontal line
        pdf.set_draw_color(0, 0, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        # Metadata
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(64, 64, 64)
        
        metadata = [
            f"Created: {transcript.created_at.strftime('%B %d, %Y at %H:%M %p')}",
            f"Updated: {transcript.updated_at.strftime('%B %d, %Y at %H:%M %p')}",
            f"Status: {transcript.status.upper()}",
        ]
        
        if transcript.session_duration:
            metadata.append(f"Duration: {transcript.session_duration} seconds")
        
        for line in metadata:
            pdf.cell(0, 7, line, ln=True)
        
        pdf.ln(5)
        
        # Separator
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        # Content heading
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "Transcribed Content:", ln=True)
        pdf.ln(2)
        
        # Content
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(32, 32, 32)
        
        if transcript.content:
            # Set a large enough multi_line width to handle text wrapping
            pdf.multi_cell(0, 6, transcript.content)
        else:
            pdf.cell(0, 6, "[No content]", ln=True)
        
        pdf.ln(5)
        
        # Raw content / detected signs (if available)
        if transcript.raw_content:
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
            
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, "Detected Signs (Raw Data):", ln=True)
            pdf.ln(2)
            
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(64, 64, 64)
            
            if isinstance(transcript.raw_content, list):
                for i, sign in enumerate(transcript.raw_content, 1):
                    pdf.cell(0, 6, f"{i}. {sign}", ln=True)
            elif isinstance(transcript.raw_content, dict):
                for key, value in transcript.raw_content.items():
                    pdf.multi_cell(0, 6, f"{key}: {value}")
        
        # Footer
        pdf.ln(5)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 10, f"Exported on {datetime.now().strftime('%B %d, %Y at %H:%M %p')}", 
                 align="C", ln=True)
        
        return filename, pdf.output(dest='S').encode('latin-1')


def get_export_options() -> Dict[str, str]:
    """
    Get available export formats
    
    Returns:
        Dict mapping format codes to descriptions
    """
    return {
        'txt': 'Plain Text (.txt)',
        'csv': 'Spreadsheet (.csv)',
        'pdf': 'PDF Document (.pdf)'
    }
