return {
  'nvim-telescope/telescope.nvim',
  dependencies = { 'nvim-lua/plenary.nvim' },
  config = function()
    local builtin = require("telescope.builtin")
    vim.keymap.set('n', '<leader>k', builtin.find_files, {})
    vim.keymap.set('n', '<leader>g', builtin.live_grep, {})
    vim.keymap.set('n', '<leader>s', builtin.current_buffer_fuzzy_find, {})
    vim.keymap.set('n', '<leader>o', function()
  require("telescope.builtin").lsp_document_symbols({
    truncate = false,
  })
end, {})

  end
}
