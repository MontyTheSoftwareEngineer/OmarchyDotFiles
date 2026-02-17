return {
    "numToStr/Comment.nvim",
    opts = {},
    config = function()
        require('Comment').setup()

        -- Normal mode: toggle comment on current line
vim.api.nvim_set_keymap('n', '<Leader>/', '<CMD>lua require("Comment.api").toggle.linewise.current()<CR>', { noremap = true, silent = true })

-- Visual mode: toggle comment on selection
vim.api.nvim_set_keymap('v', '<Leader>/', "<ESC><CMD>lua require('Comment.api').toggle.linewise(vim.fn.visualmode())<CR>", { noremap = true, silent = true })

    end,
}

