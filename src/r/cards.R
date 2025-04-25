# Utilities for printing portfolio cards.


#' Create a portfolio project card.
#' 
#' Adapted from: https://github.com/djnavarro/djnavarro.github.io
#' 
add_card <- function(
    img,
    name,
    text,
    link,
    link_text,
    img_alt,
    type = NA_character_,
    tools = NA_character_
) {
  img_tag <- paste0(
    '<div style="position: relative; ',
    'width: 100%; padding-top: 100%; overflow: hidden;">',
    '<img src="images/', img, '" ',
    'alt="', img_alt, '" ',
    'style="position: absolute; top: 0; left: 0; ',
    'width: 100%; height: 100%; object-fit: cover;" ',
    'class="card-img-top">',
    '</div>'
  )
  image_block <- if (!is.na(link) && !is.na(link_text)) {
    paste0('<a href="', link, '">', img_tag, '</a>')
  } else {
    img_tag
  }
  type_tag <- if (!is.na(type)) {
    paste0('<span class="badge bg-secondary me-1">', type, '</span>')
  } else {
    ""
  }
  tools_tag <- if (!is.na(tools)) {
    paste0(
      '<small class="text-muted"><strong>Tools used:</strong> ',
      tools,
      '</small>',
      '\n'
    )
  } else {
    ""
  }
  link_button <- if (!is.na(link) & !is.na(link_text)) {
    paste0('<a href="', link, '" class="btn btn-primary">', link_text, '</a>')
  } else {
    ""
  }
  
  lines <- c(
    '<div class="g-col-12 g-col-sm-6 g-col-md-6 g-col-xl-4">',
    '<div class="card h-100">',
    image_block,
    '<div class="card-body" style="padding-top: 0rem;">',
    paste0('<h2 class="card-title">', name, '</h2>'),
    paste0('<div class="mb-1">', type_tag, '</div>'),
    paste0('<p class="card-text" style="padding-top: .5rem;">', text, '</p>'),
    '</div>',
    '<div class="card-footer">',
    paste0('<div class="mt-1">', tools_tag, '</div>'),
    link_button,
    '</div>',
    '</div>',
    '</div>'
  )
  
  cat(lines, sep="\n")
}


#' Run row-wise `add_card` on a subset of records.
#'
print_cards <- function(df, keywords) {
  pattern <- paste(keywords, collapse = "|")
  
  matches <- grepl(pattern, df$type, ignore.case = TRUE)
  filtered_df <- df[matches, , drop = FALSE]
  
  for (i in seq_len(nrow(filtered_df))) {
    row_list <- as.list(filtered_df[i, ])
    do.call(add_card, row_list)
  }
}


#' Process Pandas df for R, respecting R null character format.
#'
pd2r <- function(df) {
  df[] <- lapply(df, function(col) {
    if (is.character(col)) {
      col[col == "nan"] <- NA_character_
    }
    col
  })
  df
}
