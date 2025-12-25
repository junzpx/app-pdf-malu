import flet as ft
from pypdf import PdfReader, PdfWriter
import os

def main(page: ft.Page):
    page.title = "PDF da Patroa"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    # Variáveis de estado
    pdf_path = ft.Ref[str]()
    
    # Função para salvar o arquivo processado
    def save_pdf(e: ft.FilePickerResultEvent):
        if e.path:
            try:
                # Lógica de remoção
                reader = PdfReader(pdf_path.current)
                writer = PdfWriter()
                
                # Parse das páginas (ex: "1, 3-5")
                pages_to_delete = set()
                parts = [p.strip() for p in page_input.value.split(',') if p.strip()]
                
                for part in parts:
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        pages_to_delete.update(range(start, end + 1))
                    else:
                        pages_to_delete.add(int(part))

                # Processar
                for i in range(len(reader.pages)):
                    if (i + 1) not in pages_to_delete:
                        writer.add_page(reader.pages[i])

                # Salvar no caminho escolhido pelo FilePicker
                output_path = e.path 
                # O FilePicker do Android às vezes não põe a extensão
                if not output_path.endswith(".pdf"):
                    output_path += ".pdf"
                    
                with open(output_path, "wb") as f:
                    writer.write(f)
                
                status_text.value = f"Sucesso! Salvo em: {output_path}"
                status_text.color = "green"
                status_text.update()
                
            except Exception as error:
                status_text.value = f"Erro: {str(error)}"
                status_text.color = "red"
                status_text.update()

    # Função chamada ao selecionar o arquivo original
    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            pdf_path.current = e.files[0].path
            selected_file_text.value = e.files[0].name
            selected_file_text.update()
            process_btn.disabled = False
            process_btn.update()

    # File Pickers
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    save_file_dialog = ft.FilePicker(on_result=save_pdf)
    
    page.overlay.extend([pick_files_dialog, save_file_dialog])

    # Elementos da UI
    selected_file_text = ft.Text("Nenhum arquivo selecionado", italic=True)
    
    page_input = ft.TextField(
        label="Páginas para remover (ex: 1, 3-5)",
        keyboard_type=ft.KeyboardType.TEXT,
        hint_text="Use vírgula ou hífen"
    )
    
    status_text = ft.Text("")

    process_btn = ft.ElevatedButton(
        "Salvar Novo PDF",
        icon=ft.icons.SAVE,
        disabled=True,
        on_click=lambda _: save_file_dialog.save_file(
            dialog_title="Salvar PDF Limpo",
            file_name="arquivo_limpo.pdf",
            allowed_extensions=["pdf"]
        )
    )

    # Layout
    page.add(
        ft.Column(
            [
                ft.Icon(ft.icons.PICTURE_AS_PDF, size=60, color=ft.colors.RED_500),
                ft.Text("Removedor de Páginas", size=24, weight="bold"),
                ft.Divider(),
                ft.ElevatedButton(
                    "Selecionar PDF",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False, 
                        allowed_extensions=["pdf"]
                    ),
                ),
                selected_file_text,
                ft.Divider(height=20, color="transparent"),
                page_input,
                ft.Divider(height=20, color="transparent"),
                process_btn,
                status_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)