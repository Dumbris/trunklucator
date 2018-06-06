export interface Sample {
    id: number;
    data: any;
}

export interface SampleInTask {
    sample: Sample;
    isSolved: boolean;
    solution: number;
}

export interface TaskState {
    items: SampleInTask[];
    totalSolved: number;
}