export type Quote = {
    id: String,
    text: String;
    date: Date,
    author: {
        name: String,
        username: String,
        avatar: string,
    },
}