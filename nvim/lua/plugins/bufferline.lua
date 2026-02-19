return {
  "akinsho/bufferline.nvim",
  dependencies = { "nvim-tree/nvim-web-devicons" },
  event = "VeryLazy",
  config = function()
    require("bufferline").setup {
      options = {
        numbers = "ordinal", -- Show buffer numbers
        diagnostics = "nvim_lsp", -- Show LSP diagnostics in the bufferline
        separator_style = "slant", -- "slant", "padded_slant", "thick", "thin"
        show_buffer_close_icons = false,
        show_close_icon = false,
        always_show_bufferline = true,
        offsets = {
          {
            filetype = "NvimTree",
            text = "File Explorer",
            highlight = "Directory",
            text_align = "left",
          },
        },
      },
    }
  end,
}

