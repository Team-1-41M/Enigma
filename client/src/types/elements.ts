/**
 * Идентификатор какого либо элемента.
 * 
 * Так как есть возможность исчезновения элемента, есть вероятность что данный ID может быть
 * недействительным. В таком случае рекомендуется проигнорировать несуществующие элементы. Если они
 * с течением времени не исчезают, нужно записать баг и найти его самому.
 */
export type ElementID = string;

/**
 * Генерирует новый ID для нового элемента.
 * 
 * @returns{} {@link ElementID} для нового элемента.
 */
export const generateElementID = (): ElementID =>
    'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
        const r = Math.random() * 16 | 0;
        return (c == 'x' ? r : (r & 0x3) | 0x8).toString(16);
    });

/**
 * Тип элемента.
 * 
 * Используется при создании и дискриминации элементов.
 */
export const ElementType = {
    /**
     * @see {@link BlockElement}
     */
    Block: 'block',

    /**
     * @see {@link TextElement}
     */
    Text: 'text',
} as const;
export type ElementType = typeof ElementType[keyof typeof ElementType];

/**
 * Общее описание для всех элементов проекта.
 * 
 * Из очевидных - идентификатор. Менее очевидное - местоположение.
 */
export type BaseElement = {
    id: ElementID,
    type: ElementType,
    x: number,
    y: number,
    name: string,
    parent?: ElementID,
};

/**
 * Любой тип элемента, не включая {@link BaseElement}.
 */
export type AnyElement = BlockElement | TextElement;

// Block

/**
 * Блок - элемент, обрамляющий ("рамка" - "frame") другие.
 * 
 * Отображается как стилизованный прямоугольник, чьи размеры можно изменить.
 */
export type BlockElement = BaseElement & {
    type: typeof ElementType.Block,
    width: number,
    height: number,
    background: Background,
    borderRadius?: BorderRadius,
    borders?: Borders,
    shadow?: Shadow,
    // TODO layout - подумать про x,y,(width,height) дочерних элементов, ведь они должны вычисляться
};

/**
 * Создать {@link BlockElement} со значениями по-умолчанию.
 * 
 * @param id ID нового элемента.
 * @param name Имя нового элемента.
 * @returns Дефолтный {@link BlockElement} с `id` и `name`.
 */
export const createBlockElement = (
    id: ElementID,
    name: string,
): BlockElement => ({
    id,
    type: ElementType.Block,
    x: 0,
    y: 0,
    name,

    width: 100,
    height: 100,
    background: '#ffffff',
});

// Text

/**
 * Текст - элемент, содержащий текст одного стиля.
 * 
 * Отображается как стилизованный текст, с якорем (координатами) в верхней границе, по горизонтали в
 * зависимости от `alignment`.
 */
export type TextElement = BaseElement & {
    type: typeof ElementType.Text,
    content: string, // TODO подумать про WYSIWYG
    alignment: TextAlignment,
    color: Color,
    fontSize: number,
    fontFamily: FontFamily,
    fontWeight?: FontWeight,
    italic?: true,
    underline?: true,
    strikethrough?: true,
};

/**
 * Создать {@link TextElement} со значениями по-умолчанию.
 * 
 * @param id ID нового элемента.
 * @param name Имя нового элемента.
 * @returns Дефолтный {@link TextElement} с `id` и `name`.
 */
export const createTextElement = (
    id: ElementID,
    name: string,
): TextElement => ({
    id,
    type: ElementType.Text,
    x: 0,
    y: 0,
    name,

    content: '',
    alignment: 'left',
    color: '#000000',
    fontSize: 12,
    fontFamily: 'Inter',
});

//
// Common visuals
//

/**
 * Непрозрачный цвет RGB.
 */
export type ColorRGB = {
    r: number,
    g: number,
    b: number,
};

/**
 * Непрозрачный цвет в формате HEX (`#RRGGBB` или `#RGB`, а также `#RRGGBBAA` или `#RGBA`).
 */
export type ColorHEX = `#${string}`;
// i wanted `#${Hex}${Hex}${Hex}${Hex}${Hex}${Hex}` but language server gave up

/**
 * Цвет, который может быть использован как для фона, так и для текста.
 */
export type Color = ColorRGB | ColorHEX; // TODO ColorHSV, ColorRGBA, etc

//
// Block visuals
//

/**
 * Радиус скругления углов.
 * 
 * Может быть числом для всех углов или описанием каждого угла.
 */
export type BorderRadius = number | {
    topLeft: number,
    topRight: number,
    bottomRight: number,
    bottomLeft: number,
};

/**
 * Ссылка на изображение.
 */
export type Image = `url(${string})`;

/**
 * Фон блока.
 */
export type Background = Color | Image;

/**
 * Стиль линии границы блока.
 * 
 * @see {@link BorderStyle.Solid}
 * @see {@link BorderStyle.Dashed}
 * @see {@link BorderStyle.Dotted}
 */
export const BorderStyle = {
    /**
     * Сплошная линия.
     */
    Solid: 'solid',

    /**
     * Штриховая линия.
     */
    Dashed: 'dashed',

    /**
     * Пунктирная линия.
     */
    Dotted: 'dotted',
} as const;
export type BorderStyle = typeof BorderStyle[keyof typeof BorderStyle];

/**
 * Граница блока (одна сторона или все стороны одновременно).
 */
export type Border = {
    color: Color,
    width: number,
    style: BorderStyle,
};

/**
 * Описание всех границ блока.
 * 
 * Если указана только одна сторона, то она будет применена ко всем сторонам.
 */
export type Borders = Border | {
    top: Border,
    right: Border,
    bottom: Border,
    left: Border,
};

/**
 * Тень блока.
 */
export type Shadow = {
    color: Color,
    offsetX: number,
    offsetY: number,
    blur: number,
    spread: number,
};

//
// Text visuals
//

/**
 * Расположение текста относительно якоря (координат).
 * 
 * @see {@link TextAlignment.Left}
 * @see {@link TextAlignment.Center}
 * @see {@link TextAlignment.Right}
 */
export const TextAlignment = {
    /**
     * Верхний левый угол текста совпадает с координатами текста (текст располагается справа от
     * якоря).
     */
    Left: 'left',

    /**
     * Верхний центр текста совпадает с координатами текста.
     */
    Center: 'center',

    /** 
     * Верхний правый угол текста совпадает с координатами текста (текст располагается слева от
     * якоря).
     */
    Right: 'right',
} as const;
export type TextAlignment = typeof TextAlignment[keyof typeof TextAlignment];

/**
 * Семья шрифта (название).
 */
export type FontFamily = string;

/**
 * Толщина шрифта.
 */
export const FontWeight = {
    /**
     * Жирный текст (обычно `700`).
     */
    Bold: 'bold',
} as const;
export type FontWeight = typeof FontWeight[keyof typeof FontWeight];
// | '100' | '200' | '300' | '400' | '500' | '600' | '700' | '800' | '900';
