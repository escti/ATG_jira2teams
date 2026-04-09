#!/usr/bin/env perl
# ==============================================================================
# Artefato: audit.cgi (Versão 2.2 - Integração Autoglass Oracle Auto Grant)
# Arquitetura Visual: Tailwind CSS (Dark Mode), jQuery, DataTables.
# ==============================================================================

use strict;
use warnings;

print "Content-type: text/html; charset=UTF-8\n\n";

print <<'HTML';
<!DOCTYPE html>
<html lang="pt-BR" class="dark scrollbar-hide">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Autoglass Oracle Auto Grant</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: { extend: { colors: { gray: { 900: '#111827', 800: '#1f2937', 700: '#374151' } } } }
        }
    </script>
    
    <style type="text/tailwindcss">
        @layer utilities {
            .scrollbar-hide::-webkit-scrollbar { display: none; }
            .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
        }
    </style>

    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
    <style>
        .dataTables_wrapper .dataTables_length, .dataTables_wrapper .dataTables_filter, 
        .dataTables_wrapper .dataTables_info, .dataTables_wrapper .dataTables_processing, 
        .dataTables_wrapper .dataTables_paginate { color: #9ca3af !important; }
        .dataTables_wrapper select, .dataTables_wrapper input { background-color: #1f2937 !important; color: white !important; border: 1px solid #374151; border-radius: 4px; padding: 4px; }
        table.dataTable tbody tr { background-color: transparent !important; }
        table.dataTable.no-footer { border-bottom: 1px solid #374151 !important; }
        .dataTables_wrapper .dataTables_paginate .paginate_button { color: #d1d5db !important; }
        .dataTables_wrapper .dataTables_paginate .paginate_button.current, 
        .dataTables_wrapper .dataTables_paginate .paginate_button.current:hover { background: #374151 !important; color: white !important; border-color: #4b5563 !important; }
    </style>
</head>
<body class="bg-gray-900 text-gray-100 font-sans antialiased min-h-screen flex flex-col scrollbar-hide">
    
    <header class="bg-gray-800 border-b border-gray-700 p-4 shadow-md">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold tracking-wider text-white">
                <span class="text-blue-500">Autoglass Oracle Auto Grant</span>
            </h1>
            <div class="flex items-center space-x-4">
                <span class="px-3 py-1 bg-gray-700 text-xs rounded-full border border-gray-600">Segurança Ativada</span>
                <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center font-bold shadow-[0_0_10px_rgba(59,130,246,0.5)]">AG</div>
            </div>
        </div>
    </header>

    <main class="flex-grow container mx-auto p-6">
        <div class="bg-gray-800 rounded-lg p-6 mb-8 border border-gray-700 shadow-lg">
            <h2 class="text-lg font-semibold mb-4 text-gray-200 border-b border-gray-700 pb-2">Central de Concessão de Privilégios</h2>
            <form class="grid grid-cols-1 md:grid-cols-6 gap-4" id="grantForm">
                <div class="col-span-1">
                    <label class="block text-xs text-blue-400 font-bold mb-1">Chamado Jira *</label>
                    <input type="text" id="jiraTicket" placeholder="INFRA-123" class="w-full bg-gray-900 border border-gray-600 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500 transition-colors" required>
                </div>
                <div class="col-span-1">
                    <label class="block text-xs text-gray-400 mb-1">Usuário Destino *</label>
                    <input type="text" id="targetUser" placeholder="EX: C_THIAGO" class="w-full bg-gray-900 border border-gray-600 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500 transition-colors uppercase" required>
                </div>
                <div class="col-span-1">
                    <label class="block text-xs text-gray-400 mb-1">Privilégio *</label>
                    <select id="privilegeType" class="w-full bg-gray-900 border border-gray-600 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500 transition-colors">
                        <option value="SELECT">SELECT</option>
                        <option value="INSERT">INSERT</option>
                        <option value="UPDATE">UPDATE</option>
                        <option value="DELETE">DELETE</option>
                    </select>
                </div>
                <div class="col-span-2">
                    <label class="block text-xs text-gray-400 mb-1">Objeto (SCHEMA.TABELA) *</label>
                    <input type="text" id="dbObject" placeholder="EX: HR.EMPLOYEES" class="w-full bg-gray-900 border border-gray-600 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500 transition-colors uppercase" required>
                </div>
                <div class="col-span-1 flex items-end">
                    <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition-colors shadow-md shadow-blue-900/50 flex justify-center items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                        Conceder
                    </button>
                </div>
            </form>
        </div>

        <div class="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-lg overflow-hidden">
            <h2 class="text-lg font-semibold mb-4 text-gray-200 border-b border-gray-700 pb-2">Log de Auditoria e Revogação</h2>
            <div class="overflow-x-auto scrollbar-hide pb-4">
                <table id="auditTable" class="w-full text-left border-collapse whitespace-nowrap">
                    <thead>
                        <tr class="bg-gray-900 text-gray-400 text-xs uppercase tracking-wider">
                            <th class="px-4 py-3 border-b border-gray-700">ID</th>
                            <th class="px-4 py-3 border-b border-gray-700">Chamado Jira</th>
                            <th class="px-4 py-3 border-b border-gray-700">Usuário Alvo</th>
                            <th class="px-4 py-3 border-b border-gray-700">Privilégio</th>
                            <th class="px-4 py-3 border-b border-gray-700">Objeto</th>
                            <th class="px-4 py-3 border-b border-gray-700">Solicitante</th>
                            <th class="px-4 py-3 border-b border-gray-700">Solicitação</th>
                            <th class="px-4 py-3 border-b border-gray-700">Expiração</th>
                            <th class="px-4 py-3 border-b border-gray-700">Status</th>
                            <th class="px-4 py-3 border-b border-gray-700">Log do Sistema</th>
                        </tr>
                    </thead>
                    <tbody class="text-sm">
HTML

my $table_rows = `/usr/local/bin/grant_reporter.sh`;
print $table_rows;

print <<'HTML';
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <footer class="bg-gray-900 border-t border-gray-800 p-4 mt-8">
        <div class="container mx-auto text-center text-xs text-gray-500">
            <p>&copy; 2026 Autoglass | Status da Aplicação: 
               <span class="text-green-500 font-mono ml-1 font-bold">ONLINE</span> | 
               Versão: <span class="text-blue-500 font-mono ml-1">v0.2.2</span>
            </p>
        </div>
    </footer>

    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#auditTable').DataTable({
                "order": [[ 0, "desc" ]],
                "language": { "url": "//cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json" },
                "pageLength": 10,
                "lengthMenu": [10, 25, 50, 100, 500]
            });

            $('#grantForm').on('submit', function(e) {
                e.preventDefault();
                alert('Atenção, Senhor: A interface CGI requer o módulo AJAX de ponte para invocar o grant_manager.sh de forma segura. O formulário front-end está visualmente integrado à V2.2.');
            });
        });
    </script>
</body>
</html>
HTML