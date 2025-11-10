#!/usr/bin/env python3
"""
Generador de PDFs para el Club Deportivo
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from datetime import datetime, date
import os

class ClubPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configurar estilos personalizados para el PDF"""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Subtítulos
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6
        ))
        
        # Texto pequeño
        self.styles.add(ParagraphStyle(
            name='CustomSmall',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=3
        ))
        
        # Texto de encabezado de tabla
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.white,
            alignment=TA_CENTER
        ))

    def generate_member_report(self, member, trainings=None, competitions=None):
        """Generar reporte de miembro individual"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, 
                               topMargin=72, bottomMargin=18)
        
        story = []
        
        # Encabezado
        story.extend(self._create_header("REPORTE DE MIEMBRO"))
        story.append(Spacer(1, 20))
        
        # Información personal
        story.extend(self._create_personal_info(member))
        story.append(Spacer(1, 20))
        
        # Entrenamientos
        if trainings:
            story.extend(self._create_trainings_section(trainings))
            story.append(Spacer(1, 20))
        
        # Competiciones
        if competitions:
            story.extend(self._create_competitions_section(competitions))
            story.append(Spacer(1, 20))
        
        # Pie de página
        story.extend(self._create_footer())
        
        # Construir PDF
        doc.build(story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)
        
        buffer.seek(0)
        return buffer

    def generate_activities_report(self, activities):
        """Generar reporte de actividades"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, 
                               topMargin=72, bottomMargin=18)
        
        story = []
        
        # Encabezado
        story.extend(self._create_header("REPORTE DE ACTIVIDADES"))
        story.append(Spacer(1, 20))
        
        # Tabla de actividades
        story.extend(self._create_activities_table(activities))
        story.append(Spacer(1, 20))
        
        # Pie de página
        story.extend(self._create_footer())
        
        doc.build(story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)
        
        buffer.seek(0)
        return buffer

    def generate_trainings_report(self, trainings):
        """Generar reporte de entrenamientos"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, 
                               topMargin=72, bottomMargin=18)
        
        story = []
        
        # Encabezado
        story.extend(self._create_header("REPORTE DE ENTRENAMIENTOS"))
        story.append(Spacer(1, 20))
        
        # Tabla de entrenamientos
        story.extend(self._create_trainings_table(trainings))
        story.append(Spacer(1, 20))
        
        # Pie de página
        story.extend(self._create_footer())
        
        doc.build(story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)
        
        buffer.seek(0)
        return buffer

    def generate_competitions_report(self, competitions):
        """Generar reporte de competiciones"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, 
                               topMargin=72, bottomMargin=18)
        
        story = []
        
        # Encabezado
        story.extend(self._create_header("REPORTE DE COMPETICIONES"))
        story.append(Spacer(1, 20))
        
        # Tabla de competiciones
        story.extend(self._create_competitions_table(competitions))
        story.append(Spacer(1, 20))
        
        # Pie de página
        story.extend(self._create_footer())
        
        doc.build(story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)
        
        buffer.seek(0)
        return buffer

    def generate_attendance_report(self, attendances):
        """Generar reporte de asistencias"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, 
                               topMargin=72, bottomMargin=18)
        
        story = []
        
        # Encabezado
        story.extend(self._create_header("REPORTE DE ASISTENCIAS"))
        story.append(Spacer(1, 20))
        
        # Tabla de asistencias
        story.extend(self._create_attendance_table(attendances))
        story.append(Spacer(1, 20))
        
        # Pie de página
        story.extend(self._create_footer())
        
        doc.build(story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)
        
        buffer.seek(0)
        return buffer

    def _create_header(self, title):
        """Crear encabezado del PDF"""
        elements = []
        
        # Título del club
        elements.append(Paragraph("CLUB DEPORTIVO", self.styles['CustomTitle']))
        elements.append(Paragraph(title, self.styles['CustomHeading']))
        elements.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.styles['CustomSmall']))
        
        return elements

    def _create_personal_info(self, member):
        """Crear sección de información personal"""
        elements = []
        
        elements.append(Paragraph("INFORMACIÓN PERSONAL", self.styles['CustomHeading']))
        
        data = [
            ['Nombre:', f"{member.nombre} {member.apellido}"],
            ['Email:', member.email],
            ['Rol:', member.rol.nombre_rol if member.rol else 'No asignado'],
            ['Fecha de Nacimiento:', member.fecha_nacimiento.strftime('%d/%m/%Y') if member.fecha_nacimiento else 'No especificada']
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ]))
        
        elements.append(table)
        return elements

    def _create_trainings_section(self, trainings):
        """Crear sección de entrenamientos"""
        elements = []
        
        elements.append(Paragraph("ENTRENAMIENTOS", self.styles['CustomHeading']))
        
        if not trainings:
            elements.append(Paragraph("No hay entrenamientos registrados.", self.styles['CustomNormal']))
            return elements
        
        data = [['Fecha', 'Actividad', 'Entrenador', 'Asistencia']]
        
        for training in trainings:
            asistencia = "Sí" if hasattr(training, 'presente') and training.presente else "No"
            data.append([
                training.fecha.strftime('%d/%m/%Y') if hasattr(training, 'fecha') else 'N/A',
                training.actividad.nombre_actividad if hasattr(training, 'actividad') and training.actividad else 'N/A',
                f"{training.entrenador.nombre} {training.entrenador.apellido}" if hasattr(training, 'entrenador') and training.entrenador else 'N/A',
                asistencia
            ])
        
        table = Table(data, colWidths=[1.5*inch, 2*inch, 2*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements

    def _create_competitions_section(self, competitions):
        """Crear sección de competiciones"""
        elements = []
        
        elements.append(Paragraph("COMPETICIONES", self.styles['CustomHeading']))
        
        if not competitions:
            elements.append(Paragraph("No hay competiciones registradas.", self.styles['CustomNormal']))
            return elements
        
        data = [['Fecha', 'Nombre', 'Ubicación', 'Actividad']]
        
        for comp in competitions:
            data.append([
                comp.fecha.strftime('%d/%m/%Y') if hasattr(comp, 'fecha') else 'N/A',
                comp.nombre if hasattr(comp, 'nombre') else 'N/A',
                comp.ubicacion if hasattr(comp, 'ubicacion') and comp.ubicacion else 'No especificada',
                comp.actividad.nombre_actividad if hasattr(comp, 'actividad') and comp.actividad else 'General'
            ])
        
        table = Table(data, colWidths=[1.5*inch, 2.5*inch, 2*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements

    def _create_activities_table(self, activities):
        """Crear tabla de actividades"""
        elements = []
        
        if not activities:
            elements.append(Paragraph("No hay actividades registradas.", self.styles['CustomNormal']))
            return elements
        
        data = [['ID', 'Nombre de la Actividad']]
        
        for activity in activities:
            data.append([
                str(activity.id_actividad),
                activity.nombre_actividad
            ])
        
        table = Table(data, colWidths=[1*inch, 5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements

    def _create_trainings_table(self, trainings):
        """Crear tabla de entrenamientos"""
        elements = []
        
        if not trainings:
            elements.append(Paragraph("No hay entrenamientos registrados.", self.styles['CustomNormal']))
            return elements
        
        data = [['ID', 'Entrenador', 'Actividad', 'Fecha']]
        
        for training in trainings:
            data.append([
                str(training.id_entrenamiento),
                f"{training.entrenador.nombre} {training.entrenador.apellido}" if hasattr(training, 'entrenador') and training.entrenador else 'N/A',
                training.actividad.nombre_actividad if hasattr(training, 'actividad') and training.actividad else 'N/A',
                training.fecha.strftime('%d/%m/%Y') if hasattr(training, 'fecha') else 'N/A'
            ])
        
        table = Table(data, colWidths=[0.8*inch, 2.5*inch, 2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements

    def _create_competitions_table(self, competitions):
        """Crear tabla de competiciones"""
        elements = []
        
        if not competitions:
            elements.append(Paragraph("No hay competiciones registradas.", self.styles['CustomNormal']))
            return elements
        
        data = [['ID', 'Nombre', 'Fecha', 'Ubicación', 'Actividad']]
        
        for comp in competitions:
            data.append([
                str(comp.id_competicion),
                comp.nombre,
                comp.fecha.strftime('%d/%m/%Y') if hasattr(comp, 'fecha') else 'N/A',
                comp.ubicacion if hasattr(comp, 'ubicacion') and comp.ubicacion else 'No especificada',
                comp.actividad.nombre_actividad if hasattr(comp, 'actividad') and comp.actividad else 'General'
            ])
        
        table = Table(data, colWidths=[0.8*inch, 2*inch, 1.2*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkorange),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements

    def _create_attendance_table(self, attendances):
        """Crear tabla de asistencias"""
        elements = []
        
        if not attendances:
            elements.append(Paragraph("No hay asistencias registradas.", self.styles['CustomNormal']))
            return elements
        
        data = [['Miembro', 'Entrenamiento', 'Fecha', 'Presente', 'Observaciones']]
        
        for att in attendances:
            data.append([
                f"{att.miembro.nombre} {att.miembro.apellido}" if hasattr(att, 'miembro') and att.miembro else 'N/A',
                att.entrenamiento.actividad.nombre_actividad if hasattr(att, 'entrenamiento') and att.entrenamiento and att.entrenamiento.actividad else 'N/A',
                att.entrenamiento.fecha.strftime('%d/%m/%Y') if hasattr(att, 'entrenamiento') and att.entrenamiento and hasattr(att.entrenamiento, 'fecha') else 'N/A',
                "Sí" if att.presente else "No",
                att.observaciones if hasattr(att, 'observaciones') and att.observaciones else '-'
            ])
        
        table = Table(data, colWidths=[2*inch, 1.5*inch, 1*inch, 0.8*inch, 1.7*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements

    def _create_footer(self):
        """Crear pie de página"""
        elements = []
        
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("---", self.styles['CustomSmall']))
        elements.append(Paragraph("Club Deportivo - Sistema de Gestión", self.styles['CustomSmall']))
        elements.append(Paragraph(f"Página generada el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", self.styles['CustomSmall']))
        
        return elements

    def _add_page_number(self, canvas, doc):
        """Agregar número de página"""
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        page_num = canvas.getPageNumber()
        text = f"Página {page_num}"
        canvas.drawRightString(200*mm, 20*mm, text)
        canvas.restoreState()