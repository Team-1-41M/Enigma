export type Project = {
    id: number,
    title: string,
    created_at: Date,
    updated_at: Date,
    author_id: number,
    content: string
}
//TODO: сортировку по датам при фетче в сторе