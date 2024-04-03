import type { ElementID, ElementType } from "./elements";

export const SocketCommand = {
    Create: 'create',
    Delete: 'delete',
    Update: 'update',
    PutAfter: 'put',
} as const;
export type SocketCommand = typeof SocketCommand[keyof typeof SocketCommand];

export type BaseSocketMessage = {
    command: SocketCommand,
};

export type AnySocketMessage = CreateSocketMessage | DeleteSocketMessage | UpdateSocketMessage | PutAfterMessage;

export type CreateSocketMessage = BaseSocketMessage & {
    command: typeof SocketCommand.Create,
    id: ElementID,
    type: ElementType,
    name: string,
};

export type DeleteSocketMessage = BaseSocketMessage & {
    command: typeof SocketCommand.Delete,
    id: ElementID,
};

export type UpdateSocketMessage = BaseSocketMessage & {
    command: typeof SocketCommand.Update,
    id: ElementID,
    [key: string]: any,
};

export type PutAfterMessage = BaseSocketMessage & {
    command: typeof SocketCommand.PutAfter,
    id: ElementID,
    after?: ElementID,
};