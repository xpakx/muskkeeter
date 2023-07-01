export type TweetDetails = {
    id: number;
    text: String;
    favs: number,
    quotes: number,
    replies: number,
    retweets: number,
    date: Date,
    retweeted: boolean,
    author: {
        name: String,
        username: String,
        avatar: string,
    },
    images?: string[]
}