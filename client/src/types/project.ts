/**
 * Идентификатор проекта.
 */
export type ProjectID = number;

/**
 * Описание проекта (метаданные).
 */
export type Project = {
    id: ProjectID,
    title: string,
    created_at: Date,
    updated_at: Date,
    author_id: number,
};
//TODO: сортировку по датам при фетче в сторе