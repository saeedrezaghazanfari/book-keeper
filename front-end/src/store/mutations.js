export default {
    SAVE_USER_DATA(state, data) {
        state.user = data;
    },
    CHANGE_BG_CLASS(state, theme) {
        state.bg_class = theme;
    },
    SAVE_SEARCH_QUERY(state, text) {
        state.search_query = text;
    },
}